if __name__ == "__main__":
    import cffi

    ffi = cffi.FFI()
    ffi.cdef(
        r"""
        typedef uint32_t UInt32;
        typedef UInt32 CFStringEncoding;
        typedef enum {
            kCFStringEncodingUTF8 = 0x08000100, /* kTextEncodingUnicodeDefault + kUnicodeUTF8Format */
        };

        typedef const void * CFTypeRef;
        typedef const struct __CFAllocator *CFAllocatorRef;
        typedef const struct __CFString *CFStringRef;

        CFStringRef CFStringCreateWithCString (CFAllocatorRef alloc, const char *cStr, CFStringEncoding encoding);
        void CFRelease ( CFTypeRef cf );

        void CoreDockSendNotification(CFStringRef notification, void *ignored);
        """,
        packed=1,
    )

    ffi.set_source("dock_spi", None)
    ffi.emit_python_code("dock_spi.py")
