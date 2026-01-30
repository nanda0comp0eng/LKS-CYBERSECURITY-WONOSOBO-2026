package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

// mixFlag implements the obfuscation logic found in the Ghidra analysis
func mixFlag(input string) string {
	length := len(input)
	// Convert string to mutable byte slice
	result := []byte(input)

	// --- PHASE 1: Shifting Characters ---
	// Ghidra: *(char *)(Result + i) = *(char *)(Input + i) + -3;
	// We subtract 3 from every ASCII character.
	for i := 0; i < length; i++ {
		result[i] = result[i] - 3
	}

	// --- PHASE 2: Swapping Characters ---
	// Ghidra Loop: for (j = 0; j < Lenght + -1; j = j + 2)
	// Logic: Swaps character at index [j] with index [(Length - 1) - (j + 1)]
	for j := 0; j < length-1; j += 2 {
		// Calculate the target index to swap with
		// iVar2 = (Lenght + -1) - (j + 1);
		targetIndex := (length - 1) - (j + 1)

		// Perform the swap if the target is within bounds
		if targetIndex >= 0 && targetIndex < length {
			temp := result[j]
			result[j] = result[targetIndex]
			result[targetIndex] = temp
		}
	}

	return string(result)
}

func main() {
	// 1. Try to open the flag.txt file
	// Matches the behavior in your first screenshot where it fails if missing
	content, err := ioutil.ReadFile("flag.txt")
	if err != nil {
		fmt.Println("a... ai?, mau gado-gado(flag.txt) yg biasa bisa??")
		return
	}

	// 2. Read content and trim standard whitespace (newlines)
	flagInput := strings.TrimSpace(string(content))

	// 3. Run the mixing algorithm
	mixedFlag := mixFlag(flagInput)

	// 4. Output the result
	// Matches output format: "Mixed Flag: ..."
	fmt.Printf("Gado-gado: %s\n", mixedFlag)
}
