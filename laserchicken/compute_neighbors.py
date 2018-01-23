from laserchicken import kd_tree, keys

def compute_sphere_neighbourhoods(env_pc, target_pc, radius):
    ''' Function to create a cylindrincal neighbourhood for a given point of
    a target point cloud among the points from an environment point cloud'''
    
    # get the kd tree for the environment point cloud
    env_tree = kd_tree.get_kdtree_for_pc(env_pc)
    
    # get a kd tree for the target point cloud
    target_tree = kd_tree.get_kdtree_for_pc(target_pc)
    
    # compute the points within an 'infinite' cylinder with a given radius
    neighb_points_indicies = target_tree.query_ball_tree(env_tree, radius)
    print("neighb_points_indicies", neighb_points_indicies)
    
    
    
    