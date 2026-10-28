# ComfyUI-AMD-MiniMaxH3

ComfyUI nodes for MiniMax H3 (Hailuo) video generation through the AMD gateway.

## Install

Search for `ComfyUI-AMD-MiniMaxH3` in ComfyUI Manager, or install it from the registry:

```bash
comfy node install amd-minimax-h3
```

To install from source instead:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/wangxunx/ComfyUI-AMD-MiniMaxH3.git
```

Restart ComfyUI. No extra Python dependencies are required.

## Configure your API key

Register at https://h3.oneclickamd.ai to get a key, then use either method below. This is a one-time setup per machine and applies to every workflow:

- Save the key to `h3_gateway_api_key.txt` in the ComfyUI user directory
- Or set the `H3_GATEWAY_API_KEY` environment variable

The file is read on every run, so dropping it in takes effect without restarting. The environment variable is read from the server process, so changing it needs a restart.

If the key is missing, the node fails immediately and tells you the registration URL and the exact file path it looked at.

### Windows, with the ComfyUI Desktop app

Use the file rather than the environment variable. Desktop launches from the Start menu and does not inherit variables you set in a PowerShell or Command Prompt session, so setting one there has no effect. Making it stick would mean `setx` or the System Properties dialog plus a full restart of Desktop.

Desktop keeps the user directory at `user` inside its install folder. That folder moves between Desktop versions and depends on what you picked during setup, so the reliable way to find it is to run the node once with no key: the error names the exact file it looked for. On one Windows install it is

```
C:\Users\<you>\AppData\Local\Comfy-Desktop\ComfyUI-Installs\ComfyUI\ComfyUI\user\h3_gateway_api_key.txt
```

Create the file there, paste the key, and save. Notepad's default encoding is fine.

Two Windows details: if File Explorer hides known extensions, **New > Text Document** already ends in `.txt`, so do not type the extension again. And do not create the file with `echo your-key > h3_gateway_api_key.txt` in Windows PowerShell, which writes UTF-16 that the node cannot read.

To point the node at a different gateway, set `H3_GATEWAY_BASE_URL`.

## Nodes

| Node | Inputs |
|---|---|
| AMD MiniMax H3 Text to Video | `prompt`, `resolution` (768P), `ratio` (six aspect ratios), `duration` (4-15 seconds) |
| AMD MiniMax H3 First-Last-Frame to Video | `first_frame`, `prompt`, `resolution` (768P), `duration` (4-15 seconds), optional `last_frame` |

Leave `last_frame` unconnected to animate a single image, or connect it to pin the final frame and animate the transition between the two. The video keeps the aspect ratio of the supplied images, so the node has no `ratio` widget. Both nodes require a prompt.

## Example workflows

In ComfyUI, open the template browser from the left sidebar, scroll to the **EXTENSIONS** section, and pick `ComfyUI-AMD-MiniMaxH3`:

| Workflow | What it does |
|---|---|
| AMD MiniMax H3 Text to Video | Prompt only |
| AMD MiniMax H3 Image to Video | Animates one image, runs as-is on the ComfyUI sample image |
| AMD MiniMax H3 First-Last-Frame to Video | Animates the transition between two images you supply |

Each workflow includes a note explaining the key setup.

## Your API key never enters a workflow

The node deliberately has no `api_key` widget. Widget values are serialized into workflow JSON and embedded into output video metadata, which would leak the key as soon as a workflow or a generated video is shared. Reading the key from the environment or from a file outside the graph keeps it out of both.

## License

MIT. See [LICENSE](LICENSE).
