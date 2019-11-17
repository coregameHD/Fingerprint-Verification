class MnMatcher:
    def __init__(self):
      pass
    #Basic operations required for Matcher
    #Swap the list in case that the input point list has longer length compared to given point list
    def listSwap(self, list1, list2):
        temp = list1
        list1 = list2
        list2 = temp
        return list1, list2

    # Translating all the points in the list to specified point
    def translateAllPoints(self, index1, index2, list1, list2):
        delta_x = list2[index2][0] - list1[index1][0] 
        delta_y = list2[index2][1] - list1[index1][1] 
        translated_point_list = []
        for i in range(len(list1)):
            new_x, new_y = self.translation(list1[i][0], list1[i][1], delta_x, delta_y)
            translated_point_list.append([new_x, new_y])
            
        return translated_point_list
    # Translate the location of a point
    def translation(self, x1,y1,delta_x, delta_y):
        x1 = x1 + delta_x
        y1 = y1 + delta_y
        return x1, y1

    def allAboutRotations(self, index1, index2, list1, list2, index_of_rotation_pts):
        # 1. translate every input points to 0,0
        all_input_pts_at_originate = self.translatePointsToOrigin(index_of_rotation_pts,list1)

        # 1.2 translate every given points to 0,0
        all_given_pts_at_originate = self.translatePointsToOrigin(index_of_rotation_pts,list2)
        
        # 2. find angle
        rotation_angle = self.findAngle(all_input_pts_at_originate[index1][0],
                                   all_input_pts_at_originate[index1][1],
                                   all_given_pts_at_originate[index2][0],
                                   all_given_pts_at_originate[index2][1])
        if(rotation_angle == 1):
            return 0
        # 3. rotate
        all_original_rotated_pts = self.rotateAllPoints(rotation_angle, all_input_pts_at_originate)

        maxs = 0
        # 4. verify rotation
        accuracy, error_rate = self.pointsVerification(all_original_rotated_pts,
                                                 all_given_pts_at_originate,
                                                 7)
        return accuracy

    # Calculate the angle between 2 points
    def findAngle(self, x1,y1,x2,y2):
        
        uv = (x1 * x2) + (y1 * y2)
        __u__ = (x1**2 + y1**2)**0.5
        __v__ = (x2**2 + y2**2)**0.5

        if(( __u__ * __v__) == 0):
            return 1
          
        cosSeta = uv / ( __u__ * __v__)
        if(cosSeta > 1 or cosSeta < -1):
            cosSeta = 1
        angle = math.acos(cosSeta)
        
        angle = (math.pi * 2) - (angle % (math.pi * 2))
        return angle

    def translatePointsToOrigin(self, index_of_rotation_pts , list1):
        pts_at_origin = []
        for i in range(len(list1)):
            new_x, new_y = self.translation(list1[i][0],list1[i][1],list1[index_of_rotation_pts][0] * -1, list1[index_of_rotation_pts][1] * -1)
            pts_at_origin.append([new_x, new_y])
        
        return pts_at_origin
        
    # Rotate all points with respect to the specified angle
    def rotateAllPoints(self, angle, list1):
        rotated_pts = []
        cos_value = (math.cos(angle))
        sin_value = (math.sin(angle))
        for i in range(len(list1)):
            new_x = round((cos_value * list1[i][0]) + (sin_value * -1 * list1[i][1]))
            new_y = round((sin_value * list1[i][0]) + (cos_value * list1[i][1]))
            rotated_pts.append([new_x, new_y])

        return rotated_pts

    # Verify the points within the fingerprint
    def pointsVerification(self, input_pts, given_pts,radius):
        total_given_pts = len(given_pts)
        total_input_pts = len(input_pts)
        match = 0
        not_match = 0

        # with radius
        never_meet = 1
        for i in range(len(input_pts)):
            for j in range(len(given_pts)):
                if((input_pts[i][0] + radius >= given_pts[j][0] and given_pts[j][0] >= input_pts[i][0] - radius)
                   and
                   (input_pts[i][1] + radius >= given_pts[j][1] and given_pts[j][1] >= input_pts[i][1] - radius)):
                    match += 1
                    never_meet = 0
                    break
                
            if(never_meet == 1):
                not_match += 1
            else:
                never_meet = 1
            
        accuracy = match/total_input_pts
        error_rate = not_match/total_input_pts
        return accuracy,error_rate
  
    def samplingPoint(self, list1, size):
        step_size = int(len(list1)/size)
        sampling_set = []
        for i in range(0,10):
            sampling_set.append(list1[i])

        for i in range(100,110):
            sampling_set.append(list1[i])
        print("SAMPLING", sampling_set)
        return sampling_set

    def createSample4Part(self, list1, list2, sample_size):
        from_each_population = round(sample_size / 4)
        sample_list = []
        for i in range(from_each_population):
            sample_list.append(list1[i])
            
        for i in range(len(list1)- from_each_population, len(list1)):
            sample_list.append(list1[i])

        for i in range(from_each_population):
            sample_list.append(list2[i])
            
        for i in range(len(list2)- from_each_population, len(list2)):
            sample_list.append(list2[i])

        print("sample: ", sample_list)
        return sample_list

    def createSample2Part(self, list1, list2, sample_size):
        from_each_population = round(sample_size / 2)
        sample_list = []
        for i in range(from_each_population):
            sample_list.append(list1[i])
        for i in range(from_each_population):
            sample_list.append(list2[i])

        print("sample: ", sample_list)
        return sample_list

    def normalSampling(self, list1, size):
        sample_list = []
        for i in range(size):
            sample_list.append(list1[i])
        return sample_list

    def sampling(self, list1, size):
      count = 0
      sample_list = []

      for i in range(len(list1)):
          if(count == size):
              break
          if(list1[i][2] == 2):
              continue
          sample_list.append(list1[i])
          count += 1
      
      return sample_list
            

    def match(self, mnSet1, mnSet2):
        input_point_list = self.sampling(mnSet1,20)
        given_point_list = self.sampling(mnSet2,20)
        
        if(len(input_point_list) > len(given_point_list)):
            print("swap list")
            input_point_list, given_point_list = self.listSwap(input_point_list,given_point_list)
        answer = 0
        maxs = 0
        for i in range(len(input_point_list)):
            for j in range(len(given_point_list)):
                translated_points = self.translateAllPoints(i,j,input_point_list,given_point_list)     
                for k in range(len(translated_points)):
                    for l in range(len(given_point_list)):   
                        similarity = self.allAboutRotations(k,l,translated_points,given_point_list, i)
                        if(similarity > maxs):
                            maxs = similarity
                        if(similarity >= 0.80):
                            maxs = similarity
                            answer = 1
                        if(answer == 1):
                            break
                    if(answer == 1):
                        break
                if(answer == 1):
                    break
            if(answer == 1):
                break    
        if(answer == 1):
            print("************************")
            print("    Fingerprint MATCH   ")
            print("************************")
        else:
            print("**************************")
            print("  Fingerprint NOT MATCH   ")
            print("**************************")
        return maxs
