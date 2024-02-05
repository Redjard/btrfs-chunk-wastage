# Btrfs Chunk Wastage Histogram

Usage:  
`btrfs-chunk-wastage.py [path to filesystem]`

Btrfs allocates itself (usually) 1 GiB sized chunks of storage space to store files on disk. As files are created, resized, and deleted, those chunks may not get filled one after another, Btrfs may accumulate partially filled chunks.  
This can cause some problems, so there are commands to split up partially filled chunks and add them into other partially filled chunks, leaving fewer more filled chunks as a result.  
For example `btrfs balance start -dusage=30 /` will split up all chunks with less than 30% space utilization.  
But when typing out such a command, it's hard to know how many chunks will be moved, how much space will be saved. Will usage=30 be enough or should you do usage=60? When do diminishing returns kick in. What sort of runtime can be expected. What is the current state of the file system?

This script will generate a histogram that can answer all those questions.

![image](https://github.com/Redjard/btrfs-chunk-wastage/assets/47570415/65d216ab-c799-404a-a4e1-5bdbe80876bd)

![image](https://github.com/Redjard/btrfs-chunk-wastage/assets/47570415/0bff0c88-eda4-470a-8907-de226d400189)

The histograms width will attempt to match your terminals width.
