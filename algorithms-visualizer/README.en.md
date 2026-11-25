# Algorithms Visualizer: Sorting & Searching

[ภาษาไทย](README.md) | **English**

A Tkinter app that animates sorting and searching algorithms step by step as coloured bar charts, so you can see each comparison and swap as it happens.

> Team mini-project for the Data Structures & Algorithms course (2025).

## Features

**Sorting tab**
- Bubble Sort, Selection Sort, Insertion Sort and Merge Sort
- Enter your own numbers (up to 20) or generate random data with a chosen count and range
- Adjustable animation speed
- Colours show unsorted, being compared and sorted elements
- Time and space complexity shown for the selected algorithm

**Searching tab**
- Sequential Search and Binary Search
- Binary Search sorts the data automatically first and highlights the current search range and midpoint
- Counts comparisons and shows the found position in both the sorted and the original data
- Summary window when the search finishes

## Complexity

| Algorithm | Time (worst) | Space |
|---|---|---|
| Bubble Sort | O(n²) | O(1) |
| Selection Sort | O(n²) | O(1) |
| Insertion Sort | O(n²) | O(1) |
| Merge Sort | O(n log n) | O(n) |
| Sequential Search | O(n) | O(1) |
| Binary Search | O(log n) | O(1) |

## How the animation works

Tkinter runs on a single event loop, so the app never sleeps inside a loop. Each algorithm is written as a step function that draws the current state and schedules the next step with `root.after(speed, ...)`, which keeps the window responsive while it animates.

Merge Sort is recursive, so it is handled differently: the app first records every intermediate array state into a list of frames, then plays the frames back one by one.

## Run

```bash
python algorithms_visualizer.py
```

Uses only the Python standard library (Tkinter, `random`).
