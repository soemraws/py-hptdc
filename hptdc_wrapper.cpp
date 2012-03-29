#include <new> // for std::nothrow
#include "tdcmanager.h"
#include "hptdc_wrapper.h"
//#include <string>
//#include <list>
#include <fstream>

char *error_string = NULL;
size_t error_string_size = 0;

const char * tdc_strerror()
{
  return error_string;
}

void tdc_set_error_string(const char * error)
{
  size_t error_size = strlen(error) + 1;
  
  // Dangerous; do some checking here!
  if (error_size > error_string_size) {
    error_string = (char*) realloc((void*) error_string, error_size);
    error_string_size = error_size;
  }

  strncpy(error_string, error, error_size);
}

tdc_manager tdc_manager_create(USHORT vendor_id,
			       USHORT device_id)
{
  return (tdc_manager) new (std::nothrow) TDCManager(vendor_id, device_id);
}

tdc_manager tdc_manager_create_default()
{
  return tdc_manager_create(0x1a13, 0x0001);
}

void tdc_manager_destroy(tdc_manager manager)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  delete ref;
}

int tdc_manager_init(tdc_manager manager)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  try {
    ref->Init();
    return 0;
  }
  catch (TDCConfigException &e) {
    tdc_set_error_string(e.errorString);
    return -1;
  }
}

int tdc_manager_cleanup(tdc_manager manager)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  try {
    ref->CleanUp();
    if (error_string != NULL)
      free(error_string);
    error_string = NULL;
    error_string_size = 0;
    return 0;
  }
  catch (TDCConfigException &e) {
    tdc_set_error_string(e.errorString);
    return -1;
  }
}

int tdc_manager_get_state(tdc_manager manager)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  return ref->GetState();
}

int tdc_manager_read_config_file(tdc_manager manager,
				   const char * filename)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  try {
    ref->ReadConfigFile(filename);
    return 0;
  }
  catch (TDCConfigException &e) {
    tdc_set_error_string(e.errorString);
    return -1;
  }
}

int tdc_manager_start(tdc_manager manager)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  try {
    ref->Start();
    return 0;
  }
  catch (TDCConfigException &e) {
    tdc_set_error_string(e.errorString);
    return -1;
  }
}

int tdc_manager_stop(tdc_manager manager)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  try {
    ref->Stop();
    return 0;
  }
  catch (TDCConfigException &e) {
    tdc_set_error_string(e.errorString);
    return -1;
  }
}

int tdc_manager_pause(tdc_manager manager)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  try {
    ref->Pause();
    return 0;
  }
  catch (TDCConfigException &e) {
    tdc_set_error_string(e.errorString);
    return -1;
  }
}

int tdc_manager_continue(tdc_manager manager)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  try {
    ref->Continue();
    return 0;
  }
  catch (TDCConfigException &e) {
    tdc_set_error_string(e.errorString);
    return -1;
  }
}

int tdc_manager_clear_buffer(tdc_manager manager)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  try {
    ref->ClearBuffer();
    return 0;
  }
  catch (TDCConfigException &e) {
    tdc_set_error_string(e.errorString);
    return -1;
  }
}

int tdc_manager_get_tdc_count(tdc_manager manager)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  return ref->GetTDCCount();
}

int tdc_manager_read(tdc_manager manager,
		     HIT * out,
		     int size)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  return ref->Read(out, size);
}

int tdc_manager_blocking_read(tdc_manager manager,
			      HIT * out,
			      int size)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  int count = 0;
  while (count < size)
    count += ref->Read(out + count, size - count);
  return count;
}

int tdc_manager_read_tdc_hit(tdc_manager manager,
			     TDCHit * buffer,
			     int length)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  return ref->ReadTDCHit(buffer, length);
}

int tdc_manager_blocking_read_tdc_hit(tdc_manager manager,
				      TDCHit * buffer,
				      int length)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  int count = 0;
  while (count < length)
    count += ref->ReadTDCHit(buffer + count, length - count);
  return count;
}

int tdc_manager_set_parameter_config(tdc_manager manager,
				     const char * config)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  return (int) ref->SetParameter(config);
}

int tdc_manager_set_parameter(tdc_manager manager,
			      const char * property,
			      const char * value)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  return (int) ref->SetParameter(property, value);
}

const char * tdc_manager_get_parameter(tdc_manager manager,
				       const char * parameter)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  return ref->GetParameter(parameter);
}

const char ** tdc_manager_get_parameter_names(tdc_manager manager,
					      int * count)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  return ref->GetParameterNames(*count);
}

int tdc_manager_get_driver_version(tdc_manager manager)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  return ref->GetDriverVersion();
}

int tdc_manager_reconfigure(tdc_manager manager)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  try {
    ref->Reconfigure();
    return 0;
  }
  catch (TDCConfigException &e) {
    tdc_set_error_string(e.errorString);
    return -1;
  }
}

TDCInfo tdc_manager_get_tdc_info(tdc_manager manager,
				 int index)
{
  TDCManager * ref = reinterpret_cast<TDCManager *>(manager);
  return ref->GetTDCInfo(index);
}

int tdc_pretty_print_hit(HIT hit, char* buffer)
{
  try {
    TDCManager::PrettyPrint(hit, buffer);
    return 0;
  }
  catch (TDCConfigException &e) {
    tdc_set_error_string(e.errorString);
    return -1;
  }
}

// This is the C++ code example from the cronologic manual.
int tdc_example_read(const char * configfile,
		     const char * outputfile,
		     int amount_to_read)
{
  TDCManager manager(0x1A13, 0x0001);
  
  try {
    manager.Init();
    manager.ReadConfigFile(configfile);
    manager.Start();
  }
  catch (TDCConfigException& e) {
    return -1;
  }

  HIT buffer[2000];
  ofstream of(outputfile, ios::out | ios::binary);
  const unsigned long res = 0x200061a8;
  of.write((const char*)&res, 4); // 25ps resolution

  while (amount_to_read > 0) {
    int count = manager.Read(buffer, 2000);
    for (int i = 0; i < count && i < amount_to_read; i++) {
      of.write((const char*) (buffer + i), sizeof(HIT));
    }
    amount_to_read -= count;
  }

  manager.Stop();
  manager.CleanUp();
  return 0;
}
