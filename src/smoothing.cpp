#include <pybind11/stl.h>

std::tuple<double, double> WeightedSum(
	const std::tuple<double, double>& t_1,
	const std::tuple<double, double>& t_2,
	const double& w_1,
	const double& w_2)
{
	return std::tuple<double, double> {
		w_1 * std::get<0>(t_1) +
			w_2 * std::get<0>(t_2),
		w_1 * std::get<1>(t_1) +
			w_2 * std::get<1>(t_2)};
}
std::tuple<double, double> WeightedSum(
	const std::tuple<double, double>& t_1,
	const std::tuple<double, double>& t_2,
	const std::tuple<double, double>& t_3,
	const double& w_1,
	const double& w_2,
	const double& w_3)
{
	return std::tuple<double, double> {
		w_1* std::get<0>(t_1) +
			w_2 * std::get<0>(t_2) +
			w_3 * std::get<0>(t_3),
		w_1* std::get<1>(t_1) +
			w_2 * std::get<1>(t_2) +
			w_3 * std::get<1>(t_3)};
}

double GetT(
	const double& t,
	const double& alpha,
	const std::tuple<double, double>& prev,
	const std::tuple<double, double>& next)
{
	double dist = pow(
		pow((std::get<0>(next) - std::get<0>(prev)), 2) +
		pow((std::get<1>(next) - std::get<1>(prev)), 2), 0.5);
	return t + pow(dist, alpha);
}

std::vector<std::tuple<double, double>> RecursiveEval(
	const std::vector<std::tuple<double, double>>& slice,
	const std::vector<double>& tangents,
	const std::vector<double>& t)
{
	std::vector<std::vector<std::tuple<double, double>>> points{ slice,
			std::vector<std::tuple<double, double>>(3),
			std::vector<std::tuple<double, double>>(2),
			std::vector<std::tuple<double, double>>(1) };
	std::vector<std::tuple<double, double>> result(t.size());
	for (int p = 0; p < t.size(); ++p) {
		for (int r = 1; r < 4; ++r) {
			int idx = std::max(r - 2, 0);
			for (int i = 0; i < (4 - r); ++i) {
				double left = (tangents.at(i + r - idx) - t.at(p)) /
					(tangents.at(i + r - idx) - tangents.at(i + idx));
				double right = (t.at(p) - tangents.at(i + idx)) /
					(tangents.at(i + r - idx) - tangents.at(i + idx));
				points.at(r).at(i) = {
					left * std::get<0>(points.at(r - 1).at(i)) +
					right * std::get<0>(points.at(r - 1).at(i + 1)),
					left * std::get<1>(points.at(r - 1).at(i)) +
					right * std::get<1>(points.at(r - 1).at(i + 1)) };
			}
		}
		result.at(p) = points.back().at(0);
	}
	return result;
}

std::vector<double> Resample(
	const double& init,
	const double& end,
	const int& subdivs) {
	double seg_length = (end - init) / (double)subdivs;
	std::vector<double> result(subdivs - 1);
	for (int i = 1; i < subdivs; ++i) {
		result.at(i - 1) = init + (double)i * seg_length;
	}
	return result;
}

bool CheckEnds(
	const std::tuple<double, double>& start,
	const std::tuple<double, double>& end) {
	return start == end;
}

std::vector<std::tuple<double, double>> Taubin(
	std::vector<std::tuple<double, double>> linestring,
	double lambda,
	double mu,
	int iters)
{
	std::vector<double> factors { lambda, mu };
	bool is_closed = CheckEnds(linestring.at(0), linestring.back());
	int size = linestring.size();
	for (int iter = 0; iter < iters; ++iter) {
		for (double factor : factors) {
			std::vector<std::tuple<double, double>> endpoints{
			linestring.at(1),
			linestring.at(size - 2) };
			std::tuple<double, double> temp_point = linestring.at(0);
			for (int i = 1; i < size - 1; ++i) {
				std::tuple<double, double> avg_point = WeightedSum(
					linestring.at(i + 1),
					linestring.at(i - 1),
					0.5, 0.5);
				linestring.at(i - 1) = temp_point;
				temp_point = WeightedSum(linestring.at(i), avg_point,
					1 - factor, factor);
			};
			linestring.at(size - 2) = temp_point;
			if (is_closed) {
				linestring.at(0) = WeightedSum(
					linestring.at(0),
					WeightedSum(endpoints.at(0), endpoints.at(1), 0.5, 0.5),
					1 - factor,
					factor);
				linestring.back() = linestring.at(0);
			}
		}	
	}
	return linestring;
}

std::vector<std::tuple<double, double>> Chaikin(
	std::vector<std::tuple<double, double>> linestring,
	int k,
	bool keep_ends)
{
	bool is_closed = CheckEnds(linestring.at(0), linestring.back());
	if (is_closed) {
		linestring.push_back(linestring.at(1));
	}
	int size = linestring.size();
	int exp = pow(2, k);
	std::vector<std::tuple<double, double>> new_linestring;
	new_linestring.reserve(exp * (size - 1) + 2);
	std::vector<double> F(exp);
	std::vector<double> G(exp);
	std::vector<double> H(exp);
	for (int j = 0; j < exp; ++j) {
		F.at(j) = .5 - .5 / exp - j * (1.0 / exp - (j + 1.0) * .5 / exp / exp);
		G.at(j) = .5 + .5 / exp + j * (1.0 / exp - (j + 1.0) / exp / exp);
		H.at(j) = j * (j + 1.0) * .5 / exp / exp;
	}
	new_linestring.push_back(linestring.at(0));
	for (int i = 1; i < size - 1; ++i) {
		for (int j = 0; j < exp; ++j) {
			new_linestring.push_back(WeightedSum(
				linestring.at(i - 1),
				linestring.at(i),
				linestring.at(i + 1),
				F.at(j),
				G.at(j),
				H.at(j)));
		}
	}
	if (keep_ends && !is_closed) {
		new_linestring.push_back(linestring.back());
	}
	else {
		new_linestring.at(0) = WeightedSum(
			linestring.at(0),
			linestring.at(1),
			0.5 * (1.0 + 1.0 / exp),
			0.5 * (1.0 - 1.0 / exp));
		if (is_closed) {
			return new_linestring;
		}
		new_linestring.push_back(WeightedSum(
			linestring.at(size - 2),
			linestring.at(size - 1),
			0.5 * (1.0 - 1.0 / exp),
			0.5 * (1.0 + 1.0 / exp)));
	}
	return new_linestring;
}

std::vector<std::tuple<double, double>> CatmullRom(
	std::vector<std::tuple<double, double>> linestring,
	double alpha,
	int subdivs)
{
	bool is_closed = CheckEnds(linestring.at(0), linestring.back());
	int size = linestring.size();
	if (is_closed) {
		linestring.insert(linestring.begin(),
			linestring.at(linestring.size() - 2));
		linestring.push_back(linestring.at(2));
	}
	else {
		linestring.insert(linestring.begin(), WeightedSum(
			linestring.at(0),
			linestring.at(1),
			2, 1));
		linestring.push_back(WeightedSum(
			linestring.back(),
			linestring.at(size - 2),
			2, 0));
	}
	std::vector<std::tuple<double, double>> new_linestring{
		linestring.at(1) };
	new_linestring.reserve(subdivs * (size - 1) + 1);
	for (int k = 0; k < linestring.size() - 3; ++k) {
		auto start = linestring.begin() + k;
		auto end = linestring.begin() + k + 4;
		std::vector<std::tuple<double, double>> slice(4);
		copy(start, end, slice.begin());
		std::vector<double> tangents{ 0 };
		for (int j = 0; j < 3; ++j) {
			tangents.push_back(
				GetT(tangents.back(), alpha,
					slice.at(j), slice.at(j + 1)));
		}
		std::vector<std::tuple<double, double>> interpolants =
			RecursiveEval(slice, tangents,
				Resample(tangents.at(1), tangents.at(2), subdivs));
		new_linestring.insert(new_linestring.end(),
			interpolants.begin(),
			interpolants.end());
		new_linestring.push_back(slice.at(2));
	}
	return new_linestring;
}