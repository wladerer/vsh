package main

import (
    "bufio"
    "fmt"
    "os"
    "regexp"
    "strings"
)

// Regular expression pattern to match the "reached required accuracy" string in the OUTCAR file
var reachedRequiredAccuracyPattern = regexp.MustCompile(`reached required accuracy`)

func main() {
    // Open the OUTCAR file in read-only mode
    outcarFile, err := os.Open("OUTCAR")
    if err != nil {
        panic(err)
    }
    defer outcarFile.Close()

    

    // Check if the OUTCAR file contains the "reached required accuracy" string
    scanner := bufio.NewScanner(outcarFile)
    reachedRequiredAccuracy := false
    for scanner.Scan() {
        if reachedRequiredAccuracyPattern.MatchString(scanner.Text()) {
            reachedRequiredAccuracy = true
            break
        }
    }

    if !reachedRequiredAccuracy {
        // The job has not reached the required accuracy, so we can restart it
        // Open the INCAR file in read-write mode
        incarFile, err := os.OpenFile("INCAR", os.O_RDWR, 0644)
        if err != nil {
            panic(err)
        }
        defer incarFile.Close()

        // Read the INCAR file line by line
        scanner = bufio.NewScanner(incarFile)
        var lines []string
        for scanner.Scan() {
            line := scanner.Text()

            // Check if the line sets the ISTART or ICHARG parameters
            if strings.HasPrefix(line, "ISTART") || strings.HasPrefix(line, "ICHARG") {
                // Replace the line with a new line that sets the ISTART or ICHARG parameter to the value needed to restart the job
                line = strings.Replace(line, "= 1", "= 0", 1)
            }
            lines = append(lines, line)
        }

        // Write the modified lines to the INCAR file
        if _, err := incarFile.Seek(0, 0); err != nil {
            panic(err)
        }
        if err := incarFile.Truncate(0); err != nil {
            panic(err)
        }
        for _, line := range lines {
            incarFile.WriteString(line + "\n")
        }

        // Inform the user that the INCAR file has been updated to restart the job
        fmt.Println("The INCAR file has been updated to restart the job.")
    }
}

