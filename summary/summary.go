package main

import (
    "bufio"
    "fmt"
    "os"
    "path/filepath"
    "regexp"
    "strconv"
    "strings"
)

// Regular expression pattern to match the "NIONS" line in the OUTCAR file
var nionsPattern = regexp.MustCompile(`NIONS\s+\d+\s+(\d+)`)

// Regular expression pattern to match the "TOTEN" line in the OUTCAR file
var totenPattern = regexp.MustCompile(`TOTEN\s+=\s+-?\d+\.\d+\s+eV\s+(-?\d+\.\d+)`)

// Regular expression pattern to match the "NELECT" line in the OUTCAR file
var nelectPattern = regexp.MustCompile(`NELECT\s+=\s+(-?\d+)`)

// Regular expression pattern to match the "NBANDS" line in the OUTCAR file
var nbandsPattern = regexp.MustCompile(`NBANDS\s+=\s+(\d+)\s+NKPTS`)

// Regular expression pattern to match the "NKPTS" line in the OUTCAR file
var nkptsPattern = regexp.MustCompile(`NKPTS\s+=\s+(\d+)`)

// Regular expression pattern to match the fourth line of the KPOINTS file
var kpointsPattern = regexp.MustCompile(`\s*(\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s+(\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s+(\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*$`)

// Regular expression pattern to match the "drift" line in the OUTCAR file
var driftPattern = regexp.MustCompile(`drift\s+=\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)`)

func main() {
    // Open the data.csv file in write mode
    dataFile, err := os.Create("data.csv")
    if err != nil {
        panic(err)
    }
    defer dataFile.Close()

    // Write the header line to the data.csv file
    dataFile.WriteString("JobType,Atoms,Energy,Electrons,Bands,NKpoints,Kx,Ky,Kz,Drift\n")
    // Get the current directory name, which will be used as the job type
    jobType := filepath.Base(filepath.Clean(os.Getenv("PWD")))

    // Open the OUTCAR file in read-only mode
    outcarFile, err := os.Open("OUTCAR")
    if err != nil {
        panic(err)
    }
    defer outcarFile.Close()

    // Open the KPOINTS file in read-only mode
    kpointsFile, err := os.Open("KPOINTS")
    if err != nil {
        panic(err)
    }
    defer kpointsFile.Close()

    // Read the OUTCAR file line by line
    outcarScanner := bufio.NewScanner(outcarFile)
    for outcarScanner.Scan() {
        line := outcarScanner.Text()

        // Check if the line contains the "NIONS" pattern
        if nionsMatch := nionsPattern.FindStringSubmatch(line); nionsMatch != nil {
            // Parse the number of atoms from the "NIONS" line
            atoms, err := strconv.ParseInt(nionsMatch[1], 10, 64)
            if err != nil {
                panic(err)
            }

            // Read the next line of the OUTCAR file
            if !outcarScanner.Scan() {
                break
            }
            line = outcarScanner.Text()

            // Check if the line contains the "TOTEN" pattern
            if totenMatch := totenPattern.FindStringSubmatch(line); totenMatch != nil {
                // Parse the energy from the "TOTEN" line
                energy, err := strconv.ParseFloat(totenMatch[1], 64)
                if err != nil {
                    panic(err)
                }

                // Read the next line of the OUTCAR file
                if !outcarScanner.Scan() {
                    break
                }
                line = outcarScanner.Text()

                // Check if the line contains the "NELECT" pattern
                if nelectMatch := nelectPattern.FindStringSubmatch(line); nelectMatch != nil {
                    // Parse the number of electrons from the "NELECT" line
                    electrons, err := strconv.ParseInt(nelectMatch[1], 10, 64)
                    if err != nil {
                        panic(err)
                    }

                    // Read the next line of the OUTCAR file
                    if !outcarScanner.Scan() {
                        break
                    }
                    line = outcarScanner.Text()
                    // Check if the line contains the "NBANDS" pattern
                    if nbandsMatch := nbandsPattern.FindStringSubmatch(line); nbandsMatch != nil {
                        // Parse the number of bands from the "NBANDS" line
                        bands, err := strconv.ParseInt(nbandsMatch[1], 10, 64)
                        if err != nil {
                            panic(err)
                        }

                        // Read the next line of the OUTCAR file
                        if !outcarScanner.Scan() {
                            break
                        }
                        line = outcarScanner.Text()

                        // Check if the line contains the "NKPTS" pattern
                        if nkptsMatch := nkptsPattern.FindStringSubmatch(line); nkptsMatch != nil {
                            // Parse the number of k-points from the "NKPTS" line
                            kpoints, err := strconv.ParseInt(nkptsMatch[1], 10, 64)
                            if err != nil {
                                panic(err)
                            }

                            // Read the next line of the KPOINTS file
                            kpointsScanner := bufio.NewScanner(kpointsFile)
                            for i := 0; i < 3; i++ {
                                if !kpointsScanner.Scan() {
                                    break
                                }
                            }
                            line = kpointsScanner.Text()

                            // Split the line into fields, and parse the Kx, Ky, and Kz values
                            fields := strings.Fields(line)
                            kx, err := strconv.ParseFloat(fields[0], 64)
                            if err != nil {
                                panic(err)
                            }
                            ky, err := strconv.ParseFloat(fields[1], 64)
                            if err != nil {
                                panic(err)
                            }
                            kz, err := strconv.ParseFloat(fields[2], 64)
                            if err != nil {
                                panic(err)
                            }

                            // Read the remaining lines of the OUTCAR file until the "drift" pattern is found
                            var drift float64
                            for outcarScanner.Scan() {
                                line = outcarScanner.Text()
                                if driftMatch := driftPattern.FindStringSubmatch(line); driftMatch != nil {
                                    // Parse the drift value from the "drift" line
                                    drift, err = strconv.ParseFloat(driftMatch[1], 64)
                                    if err != nil {
                                        panic(err)
                                    }
                                    break
                                }
                            }

                            // Append the data to the data file
                            dataFile.WriteString(fmt.Sprintf("%s,%d,%f,%d,%d,%d,%f,%f,%f,%f\n", jobType, atoms, energy, electrons, bands, kpoints, kx, ky, kz, drift))
                        }
                    }
                }
            }
        }
    }
}

