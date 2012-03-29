#ifdef WIN32
  #ifdef EXPORTING
    #define DLLIMPORT __declspec(dllexport)
  #else
    #define DLLIMPORT __declspec(dllimport)
  #endif
  #define CALL __stdcall
#else
  #define DLLIMPORT
  #define CALL
#endif

#ifdef __cplusplus
extern "C" {
#endif

  typedef unsigned short USHORT;
  typedef unsigned long ULONG;
  typedef unsigned long HIT;
  
  typedef void *tdc_manager;

  struct TDCHit;
  struct TDCInfo;

  DLLIMPORT
  const char * tdc_strerror();

  DLLIMPORT
  tdc_manager tdc_manager_create(USHORT vendor_id,
				 USHORT device_id);
  
  DLLIMPORT
  tdc_manager tdc_manager_create_default();

  DLLIMPORT
  void tdc_manager_destroy(tdc_manager manager);

  DLLIMPORT
  int tdc_manager_init(tdc_manager manager);

  DLLIMPORT
  int tdc_manager_cleanup(tdc_manager manager);

  DLLIMPORT
  int tdc_manager_get_state(tdc_manager manager);

  DLLIMPORT
  int tdc_manager_read_config_file(tdc_manager manager,
				   const char * filename);

  DLLIMPORT
  int tdc_manager_start(tdc_manager manager);

  DLLIMPORT
  int tdc_manager_stop(tdc_manager manager);

  DLLIMPORT
  int tdc_manager_pause(tdc_manager manager);

  DLLIMPORT
  int tdc_manager_continue(tdc_manager manager);

  DLLIMPORT
  int tdc_manager_clear_buffer(tdc_manager manager);

  DLLIMPORT
  int tdc_manager_get_tdc_count(tdc_manager manager);

  DLLIMPORT
  int tdc_manager_read(tdc_manager manager,
		       HIT * out,
		       int size);
  
  DLLIMPORT
  int tdc_manager_blocking_read(tdc_manager manager,
				HIT * out,
				int size);
  
  DLLIMPORT
  int tdc_manager_read_tdc_hit(tdc_manager manager,
			       TDCHit * buffer,
			       int length);

  DLLIMPORT
  int tdc_manager_blocking_read_tdc_hit(tdc_manager manager,
					TDCHit * buffer,
					int length);

  DLLIMPORT
  int tdc_manager_set_parameter_config(tdc_manager manager,
				       const char * config);
  
  DLLIMPORT
  int tdc_manager_set_parameter(tdc_manager manager,
				const char * property,
				const char * value);
  
  DLLIMPORT
  int tdc_manager_set_parameter_config(tdc_manager manager,
				       const char * config);
  
  DLLIMPORT
  const char * tdc_manager_get_parameter(tdc_manager manager,
					 const char * parameter);
  
  DLLIMPORT
  const char ** tdc_manager_get_parameter_names(tdc_manager manager,
						int * count);

  DLLIMPORT
  int tdc_manager_get_driver_version(tdc_manager manager);

  DLLIMPORT
  int tdc_manager_reconfigure(tdc_manager manager);
  
  DLLIMPORT
  int tdc_example_read(const char * configfile,
		       const char * outputfile,
		       int amount_to_read);
  
  DLLIMPORT
  int tdc_pretty_print_hit(HIT hit, char* buffer);

  DLLIMPORT
  TDCInfo tdc_manager_get_tdc_info(tdc_manager manager,
				   int index);

#ifdef __cplusplus
}
#endif
