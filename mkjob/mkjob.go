package main

import (
    "flag"
    "fmt"
    "io"
    "log"
    "os"
    "path/filepath"
)

func main() {
    // Parse the command line flags
    relaxFlag := flag.Bool("r", false, "copy the file specified by path/relax from the .vshrc directory")
    spinOrbitFlag := flag.Bool("s", false, "copy the file specified by path/spin_orbit from the .vshrc directory")
    bandFlag := flag.Bool("b", false, "copy the file specified by path/band from the .vshrc directory")
    flag.Parse()

    // Determine which file to copy based on the flags passed on the command line
    var srcPath string
    if *relaxFlag {
        srcPath = filepath.Join(os.Getenv("HOME"), ".vshrc", "relax")
    } else if *spinOrbitFlag {
        srcPath = filepath.Join(os.Getenv("HOME"), ".vshrc", "spin_orbit")
    } else if *bandFlag {
        srcPath = filepath.Join(os.Getenv("HOME"), ".vshrc", "band")
    } else {
        log.Fatal("no valid flag specified")
    }

    // Copy the file to the current directory
    srcFile, err := os.Open(srcPath)
    if err != nil {
        log.Fatal(err)
    }
    defer srcFile.Close()

    srcFilename := filepath.Base(srcPath)
    dstPath := filepath.Join(".", srcFilename)
    dstFile, err := os.Create(dstPath)
    if err != nil {
        log.Fatal(err)
    }
    defer dstFile.Close()

    _, err = io.Copy(dstFile, srcFile)
    if err != nil {
        log.Fatal(err)
    }

    fmt.Printf("file copied to %s\n", dstPath)
}

