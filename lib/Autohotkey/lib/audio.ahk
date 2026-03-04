; audio.ahk - a2 lib
; Low-level Windows audio endpoint helpers.
;
; Attribution:
; Output device switching relies on IPolicyConfig, an undocumented Windows COM
; interface reverse-engineered by EreTIk (original header: PolicyConfig.h,
; formerly at http://eretik.omegahg.com/ -- now offline). Archived here:
; https://web.archive.org/web/20131229025708/https://eretik.omegahg.com/download/PolicyConfig.h
; EreTIk's work has been the foundation of virtually every audio-switcher tool
; since ~2011. Respect. 🎩👌
;
; AHK community discussion and implementations:
;   https://www.autohotkey.com/boards/viewtopic.php?t=49980
;   https://www.autohotkey.com/boards/viewtopic.php?t=136683

/**
 * Get list of {id, name} objects for all active audio render endpoints.
 * @returns {{ name: String, path: String }[]}
 * List of {id: name} objects.
 */
audio_get_output_devices() {
    static clsid_enum := "{BCDE0395-E52F-467C-8E3D-C4579291692E}"
    static iid_enum := "{A95664D2-9614-4F35-A746-DE8DB63617E6}"

    devices := []
    try {
        imm_enum := ComObject(clsid_enum, iid_enum)
        ; EnumAudioEndpoints(eRender=0, DEVICE_STATE_ACTIVE=1)
        ComCall(3, imm_enum, "UInt", 0, "UInt", 0x1, "PtrP", &p_collection := 0)

        ; IMMDeviceCollection::GetCount
        ComCall(3, p_collection, "UIntP", &count := 0)

        loop count {
            ; IMMDeviceCollection::Item (0-based)
            ComCall(4, p_collection, "UInt", A_Index - 1, "PtrP", &p_device := 0)

            ; IMMDevice::GetId
            ComCall(5, p_device, "PtrP", &p_buf := 0)
            dev_id := StrGet(p_buf)
            DllCall("Ole32\CoTaskMemFree", "Ptr", p_buf)

            ; IMMDevice::OpenPropertyStore (STGM_READ=0)
            ComCall(4, p_device, "UInt", 0, "PtrP", &p_store := 0)

            ; PKEY_Device_FriendlyName = {A45C254E-DF1C-4EFD-8020-67D146A850E0}, 14
            key_buf := Buffer(20)
            DllCall("Ole32\CLSIDFromString",
                "Str", "{A45C254E-DF1C-4EFD-8020-67D146A850E0}",
                "Ptr", key_buf)
            NumPut("UInt", 14, key_buf, 16)

            ; IPropertyStore::GetValue -> PROPVARIANT
            prop_var := Buffer(32, 0)
            ComCall(5, p_store, "Ptr", key_buf, "Ptr", prop_var)
            dev_name := StrGet(NumGet(prop_var, 8, "Ptr"))
            DllCall("Ole32\PropVariantClear", "Ptr", prop_var)

            ObjRelease(p_store)
            ObjRelease(p_device)

            devices.Push({ id: dev_id, name: dev_name })
        }
        ObjRelease(p_collection)
    }
    return devices
}

/**
 * Get device ID string of current default render endpoint.
 * @returns {String}
 */
audio_get_default_output() {
    static clsid_enum := "{BCDE0395-E52F-467C-8E3D-C4579291692E}"
    static iid_enum := "{A95664D2-9614-4F35-A746-DE8DB63617E6}"

    default_id := ""
    try {
        imm_enum := ComObject(clsid_enum, iid_enum)
        ; GetDefaultAudioEndpoint(eRender=0, eConsole=0)
        ComCall(4, imm_enum, "UInt", 0, "UInt", 0, "PtrP", &p_device := 0)
        ComCall(5, p_device, "PtrP", &p_buf := 0)
        default_id := StrGet(p_buf)
        DllCall("Ole32\CoTaskMemFree", "Ptr", p_buf)
        ObjRelease(p_device)
    }
    return default_id
}

/**
 * Set device_id as default render endpoint for all roles.
 * @param {String} device_id - Device Id string.
 */
audio_set_default_output(device_id) {
    ; IPolicyConfig -- undocumented, stable since Vista, reverse-engineered by EreTIk
    static clsid_policy := "{870AF99C-171D-4F9E-AF0D-E63DF40C2BC9}"
    static iid_policy := "{F8679F50-850A-41CF-9C72-430F290290C8}"

    try {
        policy := ComObject(clsid_policy, iid_policy)
        ; SetDefaultEndpoint -- vTable slot 13 (0-based)
        ; Set both eConsole(0) and eCommunications(2), same as the Windows tray does
        ComCall(13, policy, "Str", device_id, "UInt", 0)
        ComCall(13, policy, "Str", device_id, "UInt", 2)
    }
}
