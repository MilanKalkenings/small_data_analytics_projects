import torch
import matplotlib.pyplot as plt
import imageio
from typing import List


def edgecase_sampling(vectors: torch.Tensor, n: int, neighborhood: float = 0.6) -> List[int]:
    """
    sample edge cases by iteratively selecting the data point most distant from the center,
    and erasing
    """
    display_ids = range(len(vectors))
    vectors_centered = vectors - torch.mean(vectors, dim=0)
    sample = []
    for i in range(n):
        # determine vector most far away from center
        magnitudes = torch.norm(vectors_centered, dim=1)
        most_dist_id = torch.argmax(magnitudes)
        magnitude_max = magnitudes[most_dist_id]
        # project all vectors to be of same length
        vectors_projected = (vectors_centered / magnitudes[:, None]) * magnitude_max
        # discard all vectors that are too close to the vector most distant from center
        # (in practice by setting their magnitude to 0 to not be considered later)
        dist = torch.norm(vectors_projected - vectors_centered[most_dist_id], dim=1)
        delete_mask = dist < (magnitude_max * neighborhood)
        vectors_centered[delete_mask] = vectors_centered[delete_mask] * 0  
        sample.append(int(most_dist_id))
        # plot intermediate state
        cancel_ids = [i for i in display_ids if delete_mask[i]]
        cancel_ids.remove(most_dist_id)
        non_canceled_ids = [i for i in display_ids if i not in cancel_ids]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(vectors[non_canceled_ids, 0], vectors[non_canceled_ids, 1], vectors[non_canceled_ids, 2], c="black", marker="o", alpha=0.1)
        ax.scatter(vectors[cancel_ids, 0], vectors[cancel_ids, 1], vectors[cancel_ids, 2], c="red", marker="o", alpha=0.2)
        ax.scatter(vectors[sample, 0], vectors[sample, 1], vectors[sample, 2], c="red", marker="*", alpha=0.5, s=120)
        ax.set_xlim([-5, 5])
        ax.set_ylim([-5, 5])
        ax.set_zlim([-5, 5])
        plt.savefig(f"{i}.png")
        display_ids = [i for i in display_ids if i not in cancel_ids]
        display_ids.remove(most_dist_id)
    # plot final state
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(vectors[non_canceled_ids, 0], vectors[non_canceled_ids, 1], vectors[non_canceled_ids, 2], c="black", marker="o", alpha=0.2)
    ax.scatter(vectors[sample, 0], vectors[sample, 1], vectors[sample, 2], c="red", marker="*", alpha=0.5, s=120)
    ax.set_xlim([-5, 5])
    ax.set_ylim([-5, 5])
    ax.set_zlim([-5, 5])
    plt.savefig(f"{i+1}.png")
    return sample


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# sample some data        
n = 8
vectors_skewed = (torch.randn(32, 3) * 1)  + torch.cat([torch.ones(32, 2) * 3, torch.zeros(32, 1)], dim=1)
vectors = torch.cat([torch.randn(5_000, 3), vectors_skewed])

# baseline: top k 
distances = torch.norm(vectors - torch.mean(vectors, dim=0), dim=1)
sample_baseline = torch.topk(distances, k=n).indices

# proposed method
sample_ids = edgecase_sampling(vectors=vectors, n=n, neighborhood=0.8)

# plot the final state VS the baseline
not_sample_ids = [i for i in range(len(vectors)) if i not in sample_ids]
not_sample_ids = [i for i in range(len(vectors)) if i not in sample_baseline]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(vectors[not_sample_ids, 0], vectors[not_sample_ids, 1], vectors[not_sample_ids, 2], c="black", marker="o", alpha=0.2)
ax.scatter(vectors[sample_ids, 0], vectors[sample_ids, 1], vectors[sample_ids, 2], c="red", marker="*", alpha=0.5, s=120, label="proposed method")
ax.scatter(vectors[sample_baseline, 0], vectors[sample_baseline, 1], vectors[sample_baseline, 2], c="blue", marker="*", alpha=0.5, s=120, label="top k")
ax.set_xlim([-5, 5])
ax.set_ylim([-5, 5])
ax.set_zlim([-5, 5])
ax.legend()
plt.savefig(f"{n+1}.png")

# create gif
filenames = [f"{i}.png" for i in range(n+2)]
with imageio.get_writer('sampling.gif', mode='I', duration=1000) as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)
