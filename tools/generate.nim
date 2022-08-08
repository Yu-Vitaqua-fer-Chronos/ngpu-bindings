#!/bin/env -S nim c --run

import std/strformat
import std/strutils
import std/sequtils
import std/json
import std/os


let
  nim_bin:string = findExe("nim")
  nimp_bin:string = findExe("nimpretty")

var flags = @["--nimcache:cache"]

if nim_bin == "" or nimp_bin == "":
  "`nim` or `nimpretty` cannot be found on PATH, please add them to the path!".quit(1)

removeDir("cache")
discard execShellCmd(&"{nim_bin} c {flags.join(\" \")} main.nim")

for file in walkDir("cache"):
  if file.path.startsWith("cache"&DirSep&"opir_") and file.path.endsWith(".json"):
    copyFile(file.path, "opir.json")
  elif file.path.startsWith("cache"&DirSep&"futhark_") and file.path.endsWith(".nim"):
    copyFile(file.path, "futharkwgpu.nim")

discard execShellCmd(&"{nimp_bin} futharkwgpu.nim")

let
  jdat = readFile("opir.json")
  jnode = parseJson(jdat)

var jnewnode:seq[JsonNode] = @[]

for node in jnode.items():
    if node["file"].getStr.contains("wgpu"):
        jnewnode.add(node)

writeFile("opir.json", pretty(%jnewnode))
