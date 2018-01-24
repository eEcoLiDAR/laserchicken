from laserchicken import utils, kd_tree, keys

def compute_cylinder_neighbourhood_indicies(env_pc, target_pc, radius):
    ''' Function to find the indicies of points within a cylindrincal neighbourhood
    for a given point of a target point cloud among the points from an environment point cloud'''

    # get the kd tree for the environment point cloud
    env_tree = kd_tree.get_kdtree_for_pc(env_pc)

    # get a kd tree for the target point cloud
    target_tree = kd_tree.get_kdtree_for_pc(target_pc)

    # compute the points within an 'infinite' cylinder with a given radius
    neighb_points_indices = target_tree.query_ball_tree(env_tree, radius)

    return neighb_points_indices

def compute_cylinder_neighbourhoods(env_pc, target_pc, radius):
    ''' Function to create a cylindrincal neighbourhood for a given point of
    a target point cloud among the points from an environment point cloud'''

    neighb_points_indices = compute_cylinder_neighbourhood_indicies(env_pc, target_pc, radius)

    return [utils.copy_pointcloud(env_pc,iarray) for iarray in neighb_points_indices]

def compute_sphere_neighbourhoods(env_pc, target_pc, radius):
    ''' Function to create a spherical neighbourhood for a given point of
    a target point cloud among the points from an environment point cloud'''

    neighb_points_indices = compute_cylinder_neighbourhood_indicies(env_pc, target_pc, radius)

    result = []
    for i in range(len(neighb_points_indices)):
        targetx,targety,targetz = utils.get_point(target_pc,i)
        cylneighbourindices = neighb_points_indices[i]
        resultindices = []
        for j in cylneighbourindices:
            envx,envy,envz = utils.get_point(env_pc,j)
            if(abs(targetz - envz) > radius): continue
            if((envx - targetx)**2 + (envy - targety)**2 + (envz - targetz)**2 <= radius**2):
                resultindices.append(j)
        result.append(utils.copy_pointcloud(env_pc,resultindices))
    return result



    return #[utils.copy_pointcloud(env_pc,iarray) for iarray in neighb_points_indices]
