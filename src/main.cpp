#include <iostream>
#include <cmath>
//test
int main(int argc, char** argv){
  std::cout << "Hello, world!" << std::endl;
  return EXIT_SUCCESS;
}

long double toRadians(const long double degree)
{
    // cmath library in C++
    // defines the constant
    // M_PI as the value of
    // pi accurate to 1e-30
    long double one_deg = (M_PI) / 180;
    return (one_deg * degree);
}
 
long double distance(long double lat1, long double long1,
                     long double lat2, long double long2)
{
    // Convert the latitudes
    // and longitudes
    // from degree to radians.
    lat1 = toRadians(lat1);
    long1 = toRadians(long1);
    lat2 = toRadians(lat2);
    long2 = toRadians(long2);
     
    // Haversine Formula
    long double dlong = long2 - long1;
    long double dlat = lat2 - lat1;
 
    long double ans = pow(sin(dlat / 2), 2) +
                          cos(lat1) * cos(lat2) *
                          pow(sin(dlong / 2), 2);
 
    ans = 2 * asin(sqrt(ans));
 
    // Radius of Earth in
    // Kilometers, R = 6371
    // Use R = 3956 for miles
    long double R = 6371;
     
    // Calculate the result
    ans = ans * R;
 
    return ans;
}

vector<double> angleFromCoordinate(double lat1, double long1, 
                                  double lat2, double long2,
                                  double al1, double al2) {
    double dLon = (long2 - long1);

    double y = sin(dLon) * cos(lat2);
    double x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dLon);

    double angle1 = atan2(y, x);

    angle1 = toDegrees(angle1);
    angle1 = (angle1 + 360) % 360;
    angle1 = 360 - angle1;

    double dist = distance(lat1, long1, lat2, long2);
    double angle2 = atan((al2 - al1) \ dist);

    return new vector<double>({angle1, angle2});
}