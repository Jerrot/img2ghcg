# Image to GitHub Contribution Graph (img2ghcg)

This script generates a GitHub commit history based on an image. Each pixel's brightness determines the number of commits on a specific date.

## Example Result
[View Example](https://github.com/Jerrot?tab=overview&from=2024-12-01&to=2024-12-31)

## Prerequisites
- The input image must be a 50x7 PNG file in RGB mode.
- Adjust the configuration part at the top of the script according to your personal needs.

## How it Works
1. The script takes an image as input.
2. It calculates the brightness of each pixel.
3. Based on the brightness, it determines the number of commits to make on specific dates.
4. The script creates a Git repository and generates commits to match the desired contribution graph.
