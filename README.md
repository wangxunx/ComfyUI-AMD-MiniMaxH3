# ComfyUI-AMD-MiniMaxH3

ComfyUI nodes for MiniMax H3 (Hailuo) video generation through the AMD gateway.

## Install

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/AMD-AIM/ComfyUI-AMD-MiniMaxH3.git
```

Restart ComfyUI. No extra Python dependencies are required.

## Configure your API key

Register at https://h3.oneclickamd.ai to get a key, then use either method below. This is a one-time setup per machine and applies to every workflow:

- Set the `H3_GATEWAY_API_KEY` environment variable
- Or save the key to `h3_gateway_api_key.txt` in the ComfyUI user directory

If the key is missing, the node fails immediately and tells you the registration URL and the exact file path.

To point the node at a different gateway, set `H3_GATEWAY_BASE_URL`.

## Nodes

| Node | Inputs |
|---|---|
| AMD MiniMax H3 Text to Video | `prompt`, `resolution` (768P / 2K), `ratio` (six aspect ratios), `duration` (4-15 seconds) |
| AMD MiniMax H3 First-Last-Frame to Video | `first_frame`, `prompt`, `resolution` (768P / 2K), `duration` (4-15 seconds), optional `last_frame` |

Leave `last_frame` unconnected to animate a single image, or connect it to pin the final frame and animate the transition between the two. The video keeps the aspect ratio of the supplied images, so the node has no `ratio` widget.

## Example workflows

The package ships ready-to-run workflows. In ComfyUI, open the template browser from the left sidebar, scroll to the **EXTENSIONS** section, and pick `ComfyUI-AMD-MiniMaxH3`. Each workflow includes a note explaining the key setup.

## Your API key never enters a workflow

The node deliberately has no `api_key` widget. Widget values are serialized into workflow JSON and embedded into output video metadata, which would leak the key as soon as a workflow or a generated video is shared. Reading the key from the environment or from a file outside the graph keeps it out of both.
