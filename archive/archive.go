package main

import (
    "bufio"
    "flag"
    "fmt"
    "io"
    "io/ioutil"
    "log"
    "os"
    "path/filepath"
    "strings"
    "time"
)

// excludePatterns is a slice of patterns that match files that should be excluded from the archive
var excludePatterns []string

func main() {
    // Parse the command line flags
    excludeFlag := flag.String("exclude", "", "a pattern that matches files that should be excluded from the archive")
    flag.Parse()

    // Add the exclude flag pattern to the list of exclude patterns
    excludePatterns = append(excludePatterns, *excludeFlag)

    // Read the exclude patterns from the .vshrc file
    vshrcPath := os.Getenv("HOME") + "/.vshrc"
    vshrcBytes, err := ioutil.ReadFile(vshrcPath)
    if err != nil {
        log.Fatal(err)
    }
    vshrc := string(vshrcBytes)
    vshrcScanner := bufio.NewScanner(strings.NewReader(vshrc))
    for vshrcScanner.Scan() {
        line := vshrcScanner.Text()
        if strings.HasPrefix(line, "exclude_pattern") {
            pattern := strings.TrimSpace(strings.TrimPrefix(line, "exclude_pattern"))
            excludePatterns = append(excludePatterns, pattern)
        }
    }

    // Create the archive filename using the current date and time
    now := time.Now()
    timestamp := now.Format("2006-01-02_15-04-05")
    archiveFilename := "archive_" + timestamp + ".tar"

    // Create a new tar archive
    archive, err := os.Create(archiveFilename)
    if err != nil {
        log.Fatal(err)
    }
    defer archive.Close()

    // Iterate over the files in the current directory and add them to the archive
    filepath.Walk(".", func(path string, info os.FileInfo, err error) error {
        // Check for any errors
        if err != nil {
            return err
        }

        // Skip directories
        if info.IsDir() {
            return nil
        }

        // Skip files that match an exclude pattern
        if matchesExcludePattern(path) {
            return nil
        }

        // Add the file to the archive
        file, err := os.Open(path)
        if err != nil {
            return err
        }
        defer file.Close()
        _, err = io.Copy(archive, file)
        if err != nil {
            return err
        }

        return nil
    })

    // Flush the contents of the archive to ensure that all data is written to the file
    err = archive.Sync()
    if err != nil {
        log.Fatal(err)
    }

    // Print a message to confirm that the archive
    fmt.Printf("The archive %s has been created.\n", archiveFilename)
}


// matchesExcludePattern checks if the given filename matches any of the exclude patterns
func matchesExcludePattern(filename string) bool {
    for _, pattern := range excludePatterns {
        if pattern == "" {
            continue
        }
        match, err := filepath.Match(pattern, filename)
        if err != nil {
            log.Fatal(err)
        }
        if match {
            return true
        }
    }
    return false
}
