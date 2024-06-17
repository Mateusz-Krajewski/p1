#include <cmath>
#include <iostream>
#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

class Calculation {
 private:
  std::vector<float> X;
  std::vector<float> Y;
  std::vector<float> Vx;
  std::vector<float> Vy;
  std::vector<float> Ax;
  std::vector<float> Ay;
 public:
  Calculation(float v0x, float v0y) {
    this->Vx.push_back(v0x);
    this->Vy.push_back(v0y);
    this->X.push_back(0);
    this->Y.push_back(0);
    this->Ax.push_back(0);
    this->Ay.push_back(0);
  }
  void Calculate(uint64_t range, float g, float b, float m, float step) {
    for (int i = 1; i < range; i++) {
        this->Ax.push_back((-b/m) * this->Vx[i-1]);
        this->Vx.push_back(this->Vx[i - 1] + this->Ax[i] * step);
        this->X.push_back(this->X[i - 1] + this->Vx[i] * step + (this->Ax[i] * step * step)/2);
    
        this->Ay.push_back((-g - (b/m)*this->Vy[i - 1]));
        this->Vy.push_back(this->Vy[i - 1] + this->Ay[i] * step);
        this->Y.push_back(this->Y[i - 1] + this->Vy[i] * step + (this->Ay[i] * step * step)/2);
        if (this->Y[this->Y.size() - 1] <= 0) {
            break;
        }
    }
  }
  std::vector<float> GetX() {
    return this->X;
  }
  std::vector<float> GetY() {
    return this->Y;
  }
  std::vector<float> GetVX() {
    return this->Vx;
  }
  std::vector<float> GetVY() {
    return this->Vy;
  }
  std::vector<float> GetAX() {
    return this->Ax;
  }
  std::vector<float> GetAY() {
    return this->Ay;
  }
};

namespace py = pybind11;

PYBIND11_MODULE(calculation, m) {
    py::class_<Calculation>(m, "Calculation")
        .def(py::init<float, float>())
        .def("Calculate", &Calculation::Calculate)
        .def("GetX", &Calculation::GetX)
        .def("GetY", &Calculation::GetY)
        .def("GetAX", &Calculation::GetAX)
        .def("GetAY", &Calculation::GetAY)
        .def("GetVX", &Calculation::GetVX)
        .def("GetVY", &Calculation::GetVY);
}