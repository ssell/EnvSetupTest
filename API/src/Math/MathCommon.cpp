#include "MathCommon.hpp"

namespace API
{
    const float PI           = 3.141592f;
    const float PI_UNDER_180 = 57.295779f;
    const float PI_OVER_180  = 0.017453f;

    float RadiansToDegrees(float const radians)
    {
        return (radians * PI_UNDER_180);
    }

    float DegreesToRadians(float const degrees)
    {
        return (degrees * PI_OVER_180);
    }
}