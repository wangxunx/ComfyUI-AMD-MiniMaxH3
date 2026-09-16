"""Text-to-video node for the AMD MiniMax H3 gateway.

The gateway issues one API key per registered user, so the key must never become part of a
workflow: widget values are serialized into workflow JSON and embedded into output file metadata,
which would leak every user's key as soon as they share a workflow or a generated video. The key
and the gateway URL are therefore read from the environment or from a file in the ComfyUI user
directory, leaving only the creative parameters in the graph.
"""

import os

import folder_paths
from comfy_api.latest import IO
from comfy_api_nodes.apis.minimax import (
    Hailuo03TaskCreationRequest,
    Hailuo03TaskCreationResponse,
    Hailuo03TaskQueryResponse,
    Hailuo03TextContent,
)
from comfy_api_nodes.util import ApiEndpoint, download_url_to_video_output, poll_op, sync_op

DEFAULT_BASE_URL = "https://h3.oneclickamd.ai"
BASE_URL_ENV_VAR = "H3_GATEWAY_BASE_URL"
API_KEY_ENV_VAR = "H3_GATEWAY_API_KEY"
API_KEY_FILENAME = "h3_gateway_api_key.txt"
REGISTRATION_URL = "https://h3.oneclickamd.ai"
FAILED_STATUSES = ["failed", "cancelled", "expired"]


def api_key_file() -> str:
    return os.path.join(folder_paths.get_user_directory(), API_KEY_FILENAME)


def resolve_api_key() -> str:
    key = os.environ.get(API_KEY_ENV_VAR, "").strip()
    if not key and os.path.isfile(api_key_file()):
        with open(api_key_file(), encoding="utf-8") as f:
            key = f.read().strip()
    if not key:
        raise Exception(
            f"No API key configured. Register at {REGISTRATION_URL} to get one, then either set the "
            f"{API_KEY_ENV_VAR} environment variable or save the key to {api_key_file()}."
        )
    return key


def resolve_base_url() -> str:
    return os.environ.get(BASE_URL_ENV_VAR, DEFAULT_BASE_URL).rstrip("/")


class AMDMiniMaxH3TextToVideo(IO.ComfyNode):
    @classmethod
    def define_schema(cls):
        return IO.Schema(
            node_id="AMDMiniMaxH3TextToVideo",
            display_name="AMD MiniMax H3 Text to Video",
            category="video/MiniMax",
            description="Generate video from a text prompt with MiniMax H3 on the AMD gateway. "
            f"Requires an account: register at {REGISTRATION_URL}, then set the {API_KEY_ENV_VAR} "
            f"environment variable or save your key to {API_KEY_FILENAME} in the ComfyUI user directory.",
            inputs=[
                IO.String.Input(
                    "prompt",
                    multiline=True,
                    default="",
                    tooltip="Text prompt for video generation.",
                ),
                IO.Combo.Input(
                    "resolution",
                    options=["768P", "2K"],
                    default="768P",
                    tooltip="Resolution of the output video.",
                ),
                IO.Combo.Input(
                    "ratio",
                    options=["16:9", "4:3", "1:1", "3:4", "9:16", "21:9"],
                    default="16:9",
                    tooltip="Aspect ratio of the output video.",
                ),
                IO.Int.Input(
                    "duration",
                    default=5,
                    min=4,
                    max=15,
                    step=1,
                    display_mode=IO.NumberDisplay.slider,
                    tooltip="Duration of the output video in seconds (4-15).",
                ),
            ],
            outputs=[IO.Video.Output()],
            hidden=[IO.Hidden.unique_id],
        )

    @classmethod
    async def execute(cls, prompt: str, resolution: str, ratio: str, duration: int) -> IO.NodeOutput:
        root = resolve_base_url()
        headers = {"Authorization": f"Bearer {resolve_api_key()}"}
        response = await sync_op(
            cls,
            ApiEndpoint(path=f"{root}/v2/video_generation", method="POST", headers=headers),
            response_model=Hailuo03TaskCreationResponse,
            data=Hailuo03TaskCreationRequest(
                model="MiniMax-H3",
                content=[Hailuo03TextContent(text=prompt)],
                resolution=resolution,
                duration=duration,
                ratio=ratio,
            ),
        )
        task_result = await poll_op(
            cls,
            ApiEndpoint(path=f"{root}/v2/query/video_generation/{response.task_id}", headers=headers),
            response_model=Hailuo03TaskQueryResponse,
            status_extractor=lambda r: r.task.status,
            failed_statuses=FAILED_STATUSES,
            poll_interval=5,
        )
        video_url = task_result.task.content.url if task_result.task.content else None
        if not video_url:
            raise Exception(f"No video URL in the response: {task_result.model_dump()}")
        return IO.NodeOutput(await download_url_to_video_output(video_url))
