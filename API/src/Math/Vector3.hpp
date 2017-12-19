#pragma once

#include <cmath>

namespace API
{
    class Vector3F 
    {
    public:

        Vector3F(float x = 0.0f, float y = 0.0f, float z = 0.0f);
        Vector3F(Vector3F const& other);
        ~Vector3F();

        float Dot(Vector3F const& other) const;

        union { float x, r, u; };
        union { float y, g, v; };
        union { float z, b, w; };

    protected:

    private:
    };
}