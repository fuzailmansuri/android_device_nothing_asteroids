#include <vector>
#include <utils/StrongPointer.h>
#include <utils/RefBase.h>
#include <binder/IBinder.h>

struct native_handle;

namespace android {

class OfflineProcClientListener : public virtual RefBase {};

class OfflineProcClient {
public:
    OfflineProcClient();
    void setListener(const sp<OfflineProcClientListener>& listener);
};

OfflineProcClient::OfflineProcClient() {}
void OfflineProcClient::setListener(const sp<OfflineProcClientListener>& listener) {}

namespace hardware {

class OfflineParameters {
public:
    virtual ~OfflineParameters();
    OfflineParameters(
        std::vector<native_handle*> a,
        std::vector<native_handle*> b,
        std::vector<int> c,
        std::vector<int> d
    );
};

OfflineParameters::~OfflineParameters() {}

OfflineParameters::OfflineParameters(
    std::vector<native_handle*> a,
    std::vector<native_handle*> b,
    std::vector<int> c,
    std::vector<int> d
) {}

class IOfflineProcService : public virtual RefBase {
public:
    static sp<IOfflineProcService> asInterface(const sp<IBinder>& binder);
};

sp<IOfflineProcService> IOfflineProcService::asInterface(const sp<IBinder>& binder) {
    return nullptr;
}

} // namespace hardware
} // namespace android
