import strutils

import futhark


proc idiomaticRenamer(name, kind, partof: string): string =
  const prefixes = @["WGPU", "Wgpu", "wgpu"]

  result = name

  for prefix in prefixes:
    result =
      if result.startsWith(prefix):
        result[prefix.len..name.high]
      else:
        result
  #[
  case result:
  of "String":
    result = "WasmInternalString"
  of "Value":
    result = "WasmValue"
  of "Result":
    result = "WasmResult"
  of "Limit":
    result = "WasmLimit"
  elif result.endsWith "Context":
    result = "Wasm" & result
  else: discard
  ]#

  case kind
  of "const", "typedef", "enum":
    discard
  else:
    result[0] = result[0].toLowerAscii

importc:
  sysPath "/data/data/com.termux/files/usr/lib/clang/14.0.0/include"
  path "."
  renameCallback idiomaticRenamer
  "wgpu-native/ffi/wgpu.h"
