#pragma once
#include <limits>

namespace API
{
    extern const float PI;
    extern const float PI_UNDER_180;
    extern const float PI_OVER_180;

    extern bool IsEqual(float a, float b, float epsilon = std::numeric_limits<float>::epsilon());
    extern bool IsZero(float a, float epsilon = std::numeric_limits<float>::epsilon());

    extern float RadiansToDegrees(float radians);
    extern float DegreesToRadians(float degrees);
}