#include <cstdint>
#include <vector>

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "Engine.h"

namespace py = pybind11;

namespace {

// Copy the engine's grid into a new (rows, cols) uint8 NumPy array.
py::array_t<uint8_t> gridToArray(const Grid& grid) {
    py::array_t<uint8_t> cells(
        std::vector<py::ssize_t>{Settings::kBoardHeight, Settings::kBoardWidth});
    auto view = cells.mutable_unchecked<2>();
    for (int row = 0; row < Settings::kBoardHeight; ++row) {
        for (int col = 0; col < Settings::kBoardWidth; ++col) {
            view(row, col) = grid.getCell(row, col);
        }
    }
    return cells;
}

}  // namespace

PYBIND11_MODULE(_core, m) {
    m.doc() = "RLTetris native core";

    py::enum_<Action>(m, "Action")
        .value("MoveLeft", Action::MoveLeft)
        .value("MoveRight", Action::MoveRight)
        .value("Rotate", Action::Rotate)
        .value("SoftDrop", Action::SoftDrop)
        .value("HardDrop", Action::HardDrop)
        .value("Hold", Action::Hold);

    py::enum_<BlockType>(m, "BlockType")
        .value("I", BlockType::I)
        .value("O", BlockType::O)
        .value("T", BlockType::T)
        .value("S", BlockType::S)
        .value("Z", BlockType::Z)
        .value("J", BlockType::J)
        .value("L", BlockType::L);

    // A read-only snapshot of a piece
    py::class_<Block>(m, "Block")
        .def_readonly("type", &Block::type)
        .def_readonly("rotation", &Block::rotationIdx)
        .def_readonly("row", &Block::row)
        .def_readonly("col", &Block::col);

    // The getters return by value
    py::class_<Engine>(m, "Engine")
        .def(py::init<unsigned int>(), py::arg("seed"))
        .def("step", &Engine::step, py::arg("action"))
        .def_property_readonly("grid",
                               [](const Engine& e) { return gridToArray(e.getGrid()); })
        .def_property_readonly("current_block",
                               [](const Engine& e) { return e.getCurrentBlock(); })
        .def_property_readonly("next_block",
                               [](const Engine& e) { return e.getNextBlock(); })
        .def_property_readonly("hold_block",
                               [](const Engine& e) { return e.getHoldBlock(); })
        .def_property_readonly("score", &Engine::getScore)
        .def_property_readonly("level", &Engine::getLevel)
        .def_property_readonly("game_over", &Engine::isGameOver)
        .def_property_readonly("ghost_row", &Engine::getGhostRow);
}
