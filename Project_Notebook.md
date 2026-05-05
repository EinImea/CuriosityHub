# Project: HyperLink (Working Title)
## Goal: Build a functional Virtual Machine manager using Apple's Virtualization Framework.

### Phase 1: The "Hello World" VM
- [ ] Research Apple's `VZVirtualMachine` documentation.
- [ ] Boot a headless (text-only) Linux kernel.
- [ ] Create a basic Swift CLI to start/stop the VM.

### Concepts to Master
1. **Hypervisors:** The layer between hardware and OS.
2. **Virtio:** The standard for virtualizing devices (disk, network).
3. **Memory Ballooning:** How the host and guest share RAM.

### Research Note: Hypervisor Types (2026-05-05)
- **Type 2 (Hosted):** Runs as an application on an existing OS (macOS). This is what Parallels, UTM, and my project are. It's easier to build because macOS handles the hardware drivers for me.
- **Type 1 (Bare Metal):** Runs directly on the hardware (like Xen or VMware ESXi). It is faster and more secure but incredibly complex to build because I would have to write drivers for the M5 chip from scratch.
- **Decision:** Stick to Type 2 using Apple's `Virtualization.framework`.

### Research Note: Hypervisor Types (2026-05-05)
- Type 2 (Hosted): Runs as an application on an existing OS. Easier to build.
- Type 1 (Bare Metal): Runs directly on hardware. More complex.
- Decision: Stick to Type 2 using Apple's Virtualization.framework.

### Phase 1.5: Guest OS Verification
- Successfully downloaded Alpine Linux aarch64 binaries.
- Location: ./GuestOS/
- Ready for Phase 2: Configuration Scripting.
## Learning Note: Mastering the Triangle of Tools.