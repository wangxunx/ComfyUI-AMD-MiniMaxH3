from typing_extensions import override

from comfy_api.latest import IO, ComfyExtension

from .nodes import AMDMiniMaxH3FirstLastFrameToVideo, AMDMiniMaxH3TextToVideo


class AMDMiniMaxH3Extension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[IO.ComfyNode]]:
        return [AMDMiniMaxH3TextToVideo, AMDMiniMaxH3FirstLastFrameToVideo]


async def comfy_entrypoint() -> AMDMiniMaxH3Extension:
    return AMDMiniMaxH3Extension()
