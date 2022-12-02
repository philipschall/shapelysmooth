std::vector<std::tuple<double, double>> Taubin(
	std::vector<std::tuple<double, double>> linestring,
	double lambda,
	double mu,
	int iters);

std::vector<std::tuple<double, double>> Chaikin(
	std::vector<std::tuple<double, double>> linestring,
	int iters,
	bool keep_ends);

std::vector<std::tuple<double, double>> CatmullRom(
	std::vector<std::tuple<double, double>> linestring,
	double alpha,
	int subdivs);