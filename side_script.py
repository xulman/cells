import pickle

from cells.processing.distance_calculating import calculate_all_mutual_distances

study = None


def main():
    global study
    load_study()
    distance_diff, energy_opt, energy_gt, max_distance_diff = avg_distance_diff(study)
    print(f"avg distance diff between optimal and truth: {distance_diff}")
    print(f"maximal distance difference is: {max_distance_diff}")
    print(f"avg distance measurements in optimal: {energy_opt}")
    print(f"avg distance measurements in truth: {energy_gt}")
    print(f"reduction is: {100 - (round(energy_opt / energy_gt, 5) * 100)}%")




def load_study():
    global study
    with open("pickle_files/masks_3D.dat", "rb") as file:
        study = pickle.Unpickler(file).load()
    study.distances = calculate_all_mutual_distances(study.cells)


def avg_distance_diff(study):
    calculations = 0
    distance_diff_sum = 0
    energy_opt_sum = 0
    energy_gt_sum = 0
    max_distance_diff = 0
    for fst_id in study.distances.keys():
        for snd_id in study.distances[fst_id].keys():
            calculations += 1
            info = study.distances[fst_id][snd_id]
            info_gt = study.distances_gt[fst_id][snd_id]
            diff = abs(info[0] - info_gt[0])
            if diff > max_distance_diff:
                max_distance_diff = diff
            distance_diff_sum += diff
            energy_opt_sum += info[1]
            energy_gt_sum += info_gt[1]
    distance_diff = round(distance_diff_sum / calculations, 5)
    energy_opt = energy_opt_sum // calculations
    energy_gt = energy_gt_sum // calculations
    return distance_diff, energy_opt, energy_gt, max_distance_diff


if __name__ == "__main__":
    main()
