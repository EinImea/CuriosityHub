import Virtualization

if #available(macOS 11.0, *) {
    if VZVirtualMachine.isSupported {
        print("✅ Success: Your M5 hardware supports Virtualization.")
    } else {
        print("❌ Error: Virtualization is not supported on this machine.")
    }
} else {
    print("❌ Error: macOS version is too old.")
}
