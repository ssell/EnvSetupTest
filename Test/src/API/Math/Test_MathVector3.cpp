#include "gtest/gtest.h"
#include "Math/Vector3.hpp"
#include "Math/MathCommon.hpp"

//------------------------------------------------------------------------------------------

class Test_Vector3 : public ::testing::Test 
{
public:

protected:

    virtual void SetUp() override
    {

    }

    virtual void TearDown() override
    {

    }

private:
};

//------------------------------------------------------------------------------------------

TEST_F(Test_Vector3, Creation)
{
    const auto x = float{ 0.0f };
    const auto y = float{ 1.0f };
    const auto z = float{ -2.0f };

    const auto base = API::Vector3F{ x, y, z };

    EXPECT_TRUE(API::IsEqual(base.x, x));
    EXPECT_TRUE(API::IsEqual(base.y, y));
    EXPECT_TRUE(API::IsEqual(base.z, z));
}

TEST_F(Test_Vector3, CopyConstructor)
{
    const auto x = float{ 0.0f };
    const auto y = float{ 1.0f };
    const auto z = float{ -2.0f };

    const auto vecA = API::Vector3F{ x, y, z };
    const auto vecB = API::Vector3F{ vecA };

    EXPECT_TRUE(API::IsEqual(vecB.x, x));
    EXPECT_TRUE(API::IsEqual(vecB.y, y));
    EXPECT_TRUE(API::IsEqual(vecB.z, z));
}

TEST_F(Test_Vector3, DotProduct)
{
    const auto vecA = API::Vector3F{ 0.0f, 1.0f, 2.0f };
    const auto vecB = API::Vector3F{ 3.0f, 4.0f, 5.0f };

    EXPECT_TRUE(API::IsEqual(vecA.Dot(vecB), 14.0f));
}