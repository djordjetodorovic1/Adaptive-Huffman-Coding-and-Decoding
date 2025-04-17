# Adaptive Huffman Coding and Decoding

This project implements multiple approaches for **adaptive Huffman coding and decoding**, where the Huffman tree evolves dynamically as data is processed. It allows encoding without prior knowledge of symbol frequencies, enabling real-time compression and decompression.

### Implemented Approaches

- **Reconstructing from Heap**  
  Rebuilds the Huffman tree from a heap of all current nodes. Repeatedly pops the two nodes with the smallest frequencies, creates a new parent whose frequency is their sum, and links the two as its children. This new parent is pushed back into the heap, and the process continues until one node remains — the root of the tree.

- **FGK Algorithm (Faller–Gallager–Knuth)**  
  Starts with a single NYT (Not Yet Transmitted) node. When a new symbol appears, it replaces the NYT with a new internal node, a leaf for the symbol, and a new NYT. For each symbol, the tree is traversed to get its bit code, then updated by increasing node frequencies and swapping nodes if necessary to preserve the sibling property.

- **Vitter's Algorithm**  
  An optimized version of FGK. Begins with a NYT node and adds new symbols similarly. Each node has an `order` value to help maintain tree structure. During updates, if the current node is a **leaf**, the algorithm looks for a swap candidate among **internal** nodes; if it's **internal**, it looks among **leaves**. It swaps nodes with the same weight and higher order, increases the weight, and continues updating up to the root.

- **Weight Blocks with Heap**  
  An approach where nodes are grouped by weight into **max-heaps** for fast access to potential swap candidates (leaders). When a new symbol is added, the NYT is expanded as before. During updates, the algorithm finds the leader with the same weight and higher order, swaps it with the current node if needed, and increases the node's weight. This structure improves the efficiency of leader lookups and tree maintenance.


**Notes:**  
This code is designed to work with ASCII characters, but it can be adapted to support other character sets.

**Disclaimer:**  
This is a research project for university purposes and is not guaranteed to be production-ready. It may contain bugs or limitations, and it should not be considered fully reliable for general use.