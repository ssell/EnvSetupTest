#include "MathCommon.hpp"
#include <cmath>

namespace API
{
    const float PI           = 3.14159265f;
    const float PI_UNDER_180 = 57.29577951f;
    const float PI_OVER_180  = 0.01745329f;

    bool IsEqual(float const a, float const b, float const epsilon)
    {
        return (std::abs(a - b) <= epsilon);
    }

    bool IsZero(float const a, float const epsilon)
    {
        return IsEqual(a, 0.0f, epsilon);
    }

    float RadiansToDegrees(float const radians)
    {
        return (radians * PI_UNDER_180);
    }

    float DegreesToRadians(float const degrees)
    {
        return (degrees * PI_OVER_180);
    }
}