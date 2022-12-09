package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	// Read the POSCAR file
	poscar, err := os.Open(os.Args[1])
	if err != nil {
		panic(err)
	}
	defer poscar.Close()

	// Create a new XYZ file
	xyz, err := os.Create("output.xyz")
	if err != nil {
		panic(err)
	}
	defer xyz.Close()

	// Read the POSCAR file line by line
	scanner := bufio.NewScanner(poscar)

	// Keep track of which line we are on
	lineNum := 0

	// Keep track of the total number of atoms
	numAtoms := 0

	// Create a slice to hold the atomic symbols
	var symbols []string
	var numSymbols []int

	for scanner.Scan() {
		line := scanner.Text()
		fields := strings.Fields(line)

		// Check if we are on the 7th line
		if lineNum == 6 {
			// Parse the number of atoms of each type
			for _, field := range fields {
				n, err := strconv.Atoi(field)
				if err != nil {
					panic(err)
				}
				numAtoms += n
				numSymbols = append(numSymbols, n)
			}

			// Update the symbols slice with the atomic symbols each type
			// so if we have 2 H and 4 Yb, the symbols slice will be ["H", "H", "Yb", "Yb", "Yb", "Yb"]
			for i, n := range numSymbols {
				for j := 0; j < n; j++ {
					symbols = append(symbols, fields[i])
				}
			}

			// Write the total number of atoms to the XYZ file
			_, err = xyz.WriteString(fmt.Sprintf("%d\n\n", numAtoms))
			if err != nil {
				panic(err)
			}
		} else if len(fields) == 3 && lineNum > 6 {
			// Parse the x, y, and z coordinates as floats
			x, err := strconv.ParseFloat(fields[0], 64)
			if err != nil {
				panic(err)
			}
			y, err := strconv.ParseFloat(fields[1], 64)
			if err != nil {
				panic(err)
			}
			z, err := strconv.ParseFloat(fields[2], 64)
			if err != nil {
				panic(err)
			}

			// Write the coordinates to the XYZ file in the format "symbol x y z" , use enumerate to get the index of the symbol
			for _, symbol := range symbols {
				_, err = xyz.WriteString(fmt.Sprintf("%s %f %f %f\n", symbol, x, y, z))
				if err != nil {
					panic(err)
				}
			}

		}

		// Increment the line number
		lineNum++
	}
}

