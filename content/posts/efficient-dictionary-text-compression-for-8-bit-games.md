Title: Efficient Dictionary-Based Text Compression for 8-Bit Games
Category: Blog
Date: 05-18-2026 23:14:00
Status: Draft

Like many 8-bit homebrew developers, I’ve always been amazed by how much story and personality classic games managed to pack into tiny cartridges. While working on my own homebrew projects, one game in particular kept haunting me: *The Legend of Zelda: Link’s Awakening*. How on earth did Nintendo fit so much rich dialogue, item descriptions, and NPC conversations into such a small Game Boy ROM?

That curiosity became the spark for this compression technique. Starting from basic ASCII and a simple bigram idea, I ended up with a flexible, highly effective dictionary method based on Dual-Tile Encoding (DTE). What began as an experiment for Game Boy quickly grew into a general-purpose solution that works great on **any 8-bit platform**.

In this deep-dive I’ll walk you through the full technique — from the basic version to the optimized 55–70%+ compression you can actually use in your own games.

---

### What is Dual-Tile Encoding (DTE)?

If you’ve spent any time in the NES, Game Boy, or broader 8-bit homebrew communities, you’ve probably encountered the term **Dual-Tile Encoding**, or **DTE** for short. It is one of the simplest yet most effective text compression techniques used in retro game development and ROM hacking.

**DTE is a form of dictionary compression** — specifically a specialized case of **byte-pair encoding (BPE)** or **digram coding**. The core idea is elegant: replace the most frequent *pairs* of characters (bigrams) in your text with a single unused byte value. During decompression, that one byte expands back into the original two characters.

### Why “Dual-Tile”?
The name originated in the **NES/Famicom** scene. On the NES, text is usually drawn using 8×8 background tiles from a pattern table. A normal character is one tile. With DTE, a single byte in the compressed string can represent *two tiles* at once. The term stuck and is now used across platforms (NES, Game Boy, ZX Spectrum, etc.), even when the graphics aren’t tile-based.

### How Basic DTE Works

1. Analyze your text on a PC. Count how often every possible two-character sequence appears.
2. Build a dictionary. Map the most common pairs to unused byte values — typically 128–255.
3. Encode by replacing matching pairs with their token.
4. Decode with a tiny routine: literal if <128, otherwise expand the pair.

**Simple pseudocode example**:

```c
const char dictionary[128][2] = { {'T','H'}, {'E',' '}, ... };

void decompress(const uint8_t* src, char* dst) {
    while (*src) {
        uint8_t b = *src++;
        if (b < 128) {
            *dst++ = b;
        } else {
            const char* pair = dictionary[b - 128];
            *dst++ = pair[0];
            *dst++ = pair[1];
        }
    }
    *dst = '\0';
}
```

---

## The Basic Technique

At its core, this compression method is **DTE implemented in the simplest possible way** — perfect for any 8-bit platform where you need to store a lot of readable text (dialogue, story, menus, etc.).

### Starting Point
We assume text is encoded as ordinary 8-bit bytes, with normal printable characters living in the range **0–127** (standard ASCII or a platform-specific charset). This leaves the entire upper half of the byte space — **128–255** — completely unused for literal characters. That gives us exactly **128 free “token” values** we can repurpose as dictionary entries.

### Step-by-Step

1. **Gather a representative corpus**  
   Collect all the text that will appear in your game (dialogue, item descriptions, menus, etc.). The more representative the sample, the better the compression.

2. **Frequency analysis**  
   On your PC, count how often every possible two-character sequence (bigram) appears.

3. **Build the dictionary**  
   Sort the bigrams by savings potential and assign the top 128 to tokens 128–255.

4. **Encoding (PC-side)**  
   Walk through the original text and replace matching bigrams with their single-byte token. Unmatched characters stay as literals.

5. **Decoding (on the target hardware)**  
   A tiny, fast routine reads the compressed stream and expands tokens on the fly.

**Platform-neutral C-style decoder**:

```c
const char dictionary[128][2] = {
    {'T','H'}, {'E',' '}, {'I','N'}, /* ... */
};

void decompress(const uint8_t* src, char* dst) {
    while (*src) {
        uint8_t b = *src++;
        if (b < 128) {
            *dst++ = (char)b;           // literal
        } else {
            const char* pair = dictionary[b - 128];
            *dst++ = pair[0];
            *dst++ = pair[1];
        }
    }
    *dst = '\0';
}
```