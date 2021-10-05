#include <i3d/image3d.h>

int main()
{
	i3d::Image3d<i3d::GRAY16> mask("data/masks_3D.tif");

	//hard-coded values for the test
	int neigh_offsets[] = {-850084, -922, -1, 1, 922, 850084};
	const int minOffset = 851007;
	const int maxOffset = 84157393;

	long long cnt = 0;
	unsigned short* p = mask.GetFirstVoxelAddr();
	long counter = 0;
	for (int o = minOffset; o < maxOffset; ++o)
	{
		long long neighs =   p[o+neigh_offsets[0]]
                         + p[o+neigh_offsets[1]]
                         + p[o+neigh_offsets[2]]
                         + p[o+neigh_offsets[3]]
                         + p[o+neigh_offsets[4]]
                         + p[o+neigh_offsets[5]];

		cnt += p[o] + neighs;
		++counter;
	}

	std::cout << "cnt=" << cnt << "\n";
	std::cout << "counter=" << counter << "\n";
	return 0;
}
