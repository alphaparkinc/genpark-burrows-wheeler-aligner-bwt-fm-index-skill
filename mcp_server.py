"""MCP stdio server for FM-Index Genomic Search."""
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from client import FMIndex

index_store = {}

def handle_rpc(request):
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "build_fm_index",
                        "description": "Index genomic sequence using FM-Index",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "sequence": {"type": "string"}
                            },
                            "required": ["name", "sequence"]
                        }
                    },
                    {
                        "name": "query_fm_index",
                        "description": "Count occurrences of pattern in indexed sequence",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "pattern": {"type": "string"}
                            },
                            "required": ["name", "pattern"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "build_fm_index":
            idx_name = args.get("name", "default")
            seq = args.get("sequence", "")
            index_store[idx_name] = FMIndex(seq)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"status": "indexed", "length": len(seq)}}
        elif name == "query_fm_index":
            idx_name = args.get("name", "default")
            pat = args.get("pattern", "")
            if idx_name not in index_store:
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": f"Index {idx_name} not found"}}
            cnt = index_store[idx_name].count(pat)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"pattern": pat, "count": cnt}}
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method {name} not found"}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": "Invalid request"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_rpc(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
