#include "Vector3.hpp"

namespace API
{
    Vector3F::Vector3F(float const x, float const y, float const z)
        : x { x }, y { y }, z { z }
    {

    }

    Vector3F::Vector3F(Vector3F const& other)
        : x { other.x }, y { other.y }, z { other.z }
    {

    }

    Vector3F::~Vector3F()
    {

    }

    float Vector3F::Dot(Vector3F const& other) const
    {
        return (x * other.x) + (y * other.y) + (z * other.z);
    }
}