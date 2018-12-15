#include <osg/Polytope>
#include <iostream>

int main()
{
    osg::Polytope pt;
    pt.setToBoundingBox(osg::BoundingBox(-1000, -1000, -1000, 1000, 1000, 1000));
    bool bContains = pt.contains(osg::Vec3(0, 0, 0));
    if (bContains)
    {
        std::cout<<"Polytope pt.contains(osg::Vec3(0, 0, 0)) has succeeded."<<std::endl;
    }
    else
    {
        std::cout<<"Polytope pt.contains(osg::Vec3(0, 0, 0)) has failed."<<std::endl;
    }
}
