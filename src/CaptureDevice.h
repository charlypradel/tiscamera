



#ifndef CAPTUREDEVICE_H_
#define CAPTUREDEVICE_H_

#include "base_types.h"

#include <vector>
#include <memory>


namespace tis_imaging
{

/**
 * @class
 */
class CaptureDevice
{

public:

    
    explicit CaptureDevice (const struct tis_device_info&);

    /**
     * @brief Creates an invalid device  
     */
    CaptureDevice ();

    CaptureDevice& operator= (const CaptureDevice&);

    /**
     * @name getInfo
     * @brief returns a struct version of the device description
     * @return struct tis_device_info
     */
    struct tis_device_info getInfo () const;
    
    std::string getName () const;

    std::string getSerial () const;
    
    enum TIS_DEVICE_TYPE getDeviceType () const;

    /**
     * @brief returns @TIS_DEVICE_TYPE string representation
     * @return std::string
     */
    std::string getDeviceTypeAsString () const;

private:

    /// internal device representation
    struct tis_device_info device;
    
}; /* class CaptureDevice */

/**
 * @name getAvailableCaptureDevices
 * @brief return a vector of all identified capture devices
 * @return std::vector<CaptureDevice>; empty on error
 */
std::vector<CaptureDevice> getAvailableCaptureDevices ();

} /* namespace tis_imaging */

#endif /* CAPTUREDEVICE_H_ */
