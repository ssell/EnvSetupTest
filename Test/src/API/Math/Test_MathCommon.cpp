#include "gtest/gtest.h"
#include "Math/MathCommon.hpp"

//------------------------------------------------------------------------------------------

class Test_MathCommon : public ::testing::Test 
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

TEST_F(Test_MathCommon, IsEqual)
{
    const auto base = float{ 5.0f };

    const auto testA = base;
    const auto testB = base - std::numeric_limits<float>::epsilon();
    const auto testC = -base;
    const auto testD = base + (std::numeric_limits<float>::epsilon() * 10.0f);
    const auto testE = base - (std::numeric_limits<float>::epsilon() * 10.0f);
    
    EXPECT_TRUE(API::IsEqual(base, testA));
    EXPECT_TRUE(API::IsEqual(base, testB));
    EXPECT_FALSE(API::IsEqual(base, testC));
    EXPECT_FALSE(API::IsEqual(base, testD));
    EXPECT_FALSE(API::IsEqual(base, testE));
}

TEST_F(Test_MathCommon, IsZero)
{
    const auto testA = float{ 0.0f };
    const auto testB = testA - std::numeric_limits<float>::epsilon();
    const auto testC = -testA;
    const auto testD = testA + (std::numeric_limits<float>::epsilon() * 10.0f);
    const auto testE = testA - (std::numeric_limits<float>::epsilon() * 10.0f);

    EXPECT_TRUE(API::IsZero(testA));
    EXPECT_TRUE(API::IsZero(testB));
    EXPECT_TRUE(API::IsZero(testC));
    EXPECT_FALSE(API::IsZero(testD));
    EXPECT_FALSE(API::IsZero(testE));
}

TEST_F(Test_MathCommon, DegreesToRadians)
{
    const auto deg0    = float{ 0.0f };
    const auto deg90   = float{ 90.0f };
    const auto deg180  = float{ 180.0f };
    const auto degN360 = float{ -360.0f };
    const auto deg450  = float{ 450.0f };

    const auto rad0    = float{ 0.0f };
    const auto rad90   = API::PI * 0.5f;
    const auto rad180  = API::PI;
    const auto radN360 = -API::PI * 2.0f;
    const auto rad450  = API::PI * 2.5f;

    const auto res = API::DegreesToRadians(degN360);
    
    EXPECT_TRUE(API::IsEqual(API::DegreesToRadians(deg0), rad0, 0.0001f));
    EXPECT_TRUE(API::IsEqual(API::DegreesToRadians(deg90), rad90, 0.0001f));
    EXPECT_TRUE(API::IsEqual(API::DegreesToRadians(deg180), rad180, 0.0001f));
    EXPECT_TRUE(API::IsEqual(API::DegreesToRadians(degN360), radN360, 0.0001f));
    EXPECT_TRUE(API::IsEqual(API::DegreesToRadians(deg450), rad450, 0.0001f));
}

TEST_F(Test_MathCommon, RadiansToDegrees)
{
    const auto rad0    = float{ 0.0f };
    const auto rad90   = API::PI * 0.5f;
    const auto rad180  = API::PI;
    const auto radN360 = -API::PI * 2.0f;
    const auto rad450  = API::PI * 2.5f;

    const auto deg0    = float{ 0.0f };
    const auto deg90   = float{ 90.0f };
    const auto deg180  = float{ 180.0f };
    const auto degN360 = float{ -360.0f };
    const auto deg450  = float{ 450.0f };
    
    EXPECT_TRUE(API::IsEqual(API::RadiansToDegrees(rad0), deg0, 0.0001f));
    EXPECT_TRUE(API::IsEqual(API::RadiansToDegrees(rad90), deg90, 0.0001f));
    EXPECT_TRUE(API::IsEqual(API::RadiansToDegrees(rad180), deg180, 0.0001f));
    EXPECT_TRUE(API::IsEqual(API::RadiansToDegrees(radN360), degN360, 0.0001f));
    EXPECT_TRUE(API::IsEqual(API::RadiansToDegrees(rad450), deg450, 0.0001f));
}