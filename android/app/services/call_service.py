from app.native.android_calls import native_calls

class CallService:
    def dial_emergency_contact(self, phone):
        native_calls.make_direct_call(phone)

call_service = CallService()
