from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.manager import ws_manager

router = APIRouter()

@router.websocket("/ws/sos/{incident_uuid}")
async def websocket_sos_stream(websocket: WebSocket, incident_uuid: str):
    await ws_manager.connect(websocket, incident_uuid)
    try:
        while True:
            data = await websocket.receive_json()
            # Broadcast received telemetry to all observers (contacts/dashboard)
            await ws_manager.broadcast_to_room(incident_uuid, data)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, incident_uuid)
