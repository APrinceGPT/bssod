/**
 * Common Windows bugcheck (BSOD) descriptions for quick reference.
 * Covers 30+ most frequent Windows crash errors.
 */
export const BUGCHECK_DESCRIPTIONS: Record<string, string> = {
  // Most Common (Top 10)
  IRQL_NOT_LESS_OR_EQUAL:
    "A kernel-mode driver attempted to access pageable memory at an invalid interrupt request level (IRQL). Often caused by faulty drivers or memory issues.",
  
  SYSTEM_THREAD_EXCEPTION_NOT_HANDLED:
    "A system thread generated an exception that the error handler did not catch. Usually indicates a driver bug or corrupted system file.",
  
  PAGE_FAULT_IN_NONPAGED_AREA:
    "The system tried to access memory that was not available or was invalid. Can indicate faulty RAM, corrupt drivers, or disk errors.",
  
  KERNEL_DATA_INPAGE_ERROR:
    "A kernel data page could not be read from the paging file or memory. Often points to disk issues, bad sectors, or failing storage.",
  
  CRITICAL_PROCESS_DIED:
    "A critical system process terminated unexpectedly. May be caused by corrupted system files, driver conflicts, or malware.",
  
  DRIVER_IRQL_NOT_LESS_OR_EQUAL:
    "A driver attempted to access memory at an invalid IRQL. The faulting driver name is usually provided in the crash details.",
  
  SYSTEM_SERVICE_EXCEPTION:
    "An exception occurred while executing a routine that transitions from non-privileged to privileged code. Often a driver or antivirus issue.",
  
  KMODE_EXCEPTION_NOT_HANDLED:
    "A kernel-mode program generated an exception which the error handler did not catch. Check for driver updates.",
  
  UNEXPECTED_KERNEL_MODE_TRAP:
    "The CPU generated a trap that the kernel was not prepared to handle. Can indicate hardware failure or memory corruption.",
  
  DRIVER_POWER_STATE_FAILURE:
    "A driver is in an inconsistent or invalid power state. Usually occurs during sleep/wake cycles with incompatible drivers.",

  // Common (11-20)
  NTFS_FILE_SYSTEM:
    "A problem occurred with the NTFS file system. May indicate disk corruption, failing drive, or file system errors.",
  
  VIDEO_TDR_FAILURE:
    "The display driver failed to respond in time. Often related to GPU driver issues or overheating graphics card.",
  
  VIDEO_TDR_TIMEOUT_DETECTED:
    "The graphics driver took too long to respond and was reset. Update or reinstall graphics drivers.",
  
  BAD_POOL_HEADER:
    "A pool header was corrupted. Usually caused by driver issues, antivirus software, or faulty RAM.",
  
  BAD_POOL_CALLER:
    "The current thread is making a bad pool request. Often indicates a driver bug.",
  
  MEMORY_MANAGEMENT:
    "A severe memory management error occurred. Can indicate RAM failure, driver bugs, or system file corruption.",
  
  WHEA_UNCORRECTABLE_ERROR:
    "A fatal hardware error was detected. Check CPU, RAM, and storage hardware for failures.",
  
  DPC_WATCHDOG_VIOLATION:
    "A DPC (Deferred Procedure Call) ran too long. Usually caused by driver bugs or incompatible software.",
  
  CLOCK_WATCHDOG_TIMEOUT:
    "A processor core did not respond in time. May indicate overclocking issues, BIOS problems, or hardware failure.",
  
  KERNEL_SECURITY_CHECK_FAILURE:
    "A critical kernel security check failed. Often caused by driver bugs, memory corruption, or incompatible software.",

  // Additional Common (21-30)
  PFN_LIST_CORRUPT:
    "The page frame number (PFN) list was corrupted. Usually indicates faulty drivers or RAM issues.",
  
  INACCESSIBLE_BOOT_DEVICE:
    "Windows cannot access the boot device. May be caused by storage driver issues, BIOS changes, or disk failures.",
  
  KERNEL_MODE_HEAP_CORRUPTION:
    "The kernel mode heap was corrupted. Indicates a serious driver or system component bug.",
  
  APC_INDEX_MISMATCH:
    "An APC (Asynchronous Procedure Call) state index was mismatched. Usually a driver synchronization issue.",
  
  REFERENCE_BY_POINTER:
    "The reference count of an object is incorrect. Often caused by driver bugs.",
  
  SPECIAL_POOL_DETECTED_MEMORY_CORRUPTION:
    "Memory corruption was detected in a special pool. Helps identify the driver causing memory overwrites.",
  
  DRIVER_OVERRAN_STACK_BUFFER:
    "A driver overran a stack-based buffer. Security vulnerability that can cause system instability.",
  
  BUGCODE_USB_DRIVER:
    "A USB driver caused a fatal error. Check USB devices and drivers.",
  
  FAT_FILE_SYSTEM:
    "A problem occurred with the FAT file system. May indicate disk corruption on FAT-formatted drives.",
  
  REGISTRY_ERROR:
    "A critical registry error occurred. May indicate registry corruption or disk issues.",

  // Additional Important (31-35)
  HAL_INITIALIZATION_FAILED:
    "The Hardware Abstraction Layer failed to initialize. Usually a boot-time hardware or driver issue.",
  
  MACHINE_CHECK_EXCEPTION:
    "The CPU detected a fatal hardware error. Often indicates CPU, motherboard, or memory failure.",
  
  ATTEMPTED_WRITE_TO_READONLY_MEMORY:
    "A driver attempted to write to read-only memory. Indicates a driver bug.",
  
  KERNEL_AUTO_BOOST_LOCK_ACQUISITION_WITH_RAISED_IRQL:
    "A lock was acquired with a raised IRQL in an improper context. Driver synchronization issue.",
  
  DRIVER_CORRUPTED_EXPOOL:
    "A driver corrupted the system pool. The faulting driver should be identified in crash details.",
};

/**
 * Get a bugcheck description by name.
 * Returns undefined if the bugcheck is not in the known list.
 */
export function getBugcheckDescription(bugcheckName: string): string | undefined {
  return BUGCHECK_DESCRIPTIONS[bugcheckName];
}
