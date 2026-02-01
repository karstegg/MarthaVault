"""
Whisper MCP Server - Modified for Cloud Deployment with HTTP Transport

This file replaces: /opt/whisper-mcp/src/mcp_server_whisper/server.py on the VM

Modifications:
- Added argparse for --transport and --port flags
- Added SSE HTTP transport for cloud accessibility
- Maintains backward compatibility with stdio transport
"""

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("whisper", dependencies=["openai", "pydub", "aiofiles"])


def main() -> None:
    """Run main entrypoint."""
    # Import and register tools at runtime (not at module import time)
    from .tools import register_all_tools
    import argparse

    parser = argparse.ArgumentParser(description="Whisper MCP Server")
    parser.add_argument("--transport", default="stdio", choices=["stdio", "http"],
                       help="Transport type: stdio for local, http for cloud deployment")
    parser.add_argument("--port", type=int, default=8082,
                       help="Port number for HTTP transport (default: 8082)")
    args = parser.parse_args()

    register_all_tools(mcp)

    if args.transport == "http":
        # HTTP transport for cloud deployment via SSE
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Route
        import uvicorn

        sse = SseServerTransport("/messages")

        async def handle_sse(request):
            async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
                await mcp.run(
                    streams[0], streams[1], mcp.create_initialization_options()
                )

        async def handle_messages(request):
            return await sse.handle_post_message(request.scope, request.receive, request._send)

        app = Starlette(
            debug=False,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Route("/messages", endpoint=handle_messages, methods=["POST"]),
            ]
        )

        print(f"Starting Whisper MCP Server on http://0.0.0.0:{args.port}")
        uvicorn.run(app, host="0.0.0.0", port=args.port, log_level="info")
    else:
        # Default stdio transport for local use
        mcp.run()


if __name__ == "__main__":
    main()
