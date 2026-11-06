#include <pybind11/pybind11.h>

#include "Engine.h"

namespace py = pybind11;

// smoke test 
// will be replaced later with a real engine binding
static int engine_smoke(unsigned int seed) {
    Engine engine(seed);
    return static_cast<int>(engine.getCurrentBlock().type);
}

PYBIND11_MODULE(_core, m) {
    m.doc() = "RLTetris native core";
    m.def("engine_smoke", &engine_smoke, py::arg("seed"),
          "Create an Engine with this seed and return its first piece (0-6).");
}
