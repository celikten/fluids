#from fluids import *
from fluids.numerics import IS_PYPY
if not IS_PYPY:
    import fluids.numba
    import numba
from datetime import datetime
import pytz
import inspect

def also_numba(f):
    if not IS_PYPY:
        f.duplicate_with_numba = True
    return f


#IS_PYPY = True
from fluids.atmosphere import ATMOSPHERE_1976, ATMOSPHERE_NRLMSISE00, airmass, solar_position, earthsun_distance, sunrise_sunset, solar_irradiation

if not IS_PYPY:
    ATMOSPHERE_1976_numba = fluids.numba.ATMOSPHERE_1976
    airmass_numba = fluids.numba.atmosphere.airmass

    @numba.njit
    def numba_int_airmass(Z):
        return fluids.numba.atmosphere.ATMOSPHERE_1976(Z, 0).rho

class BaseTimeSuite(object):
    def setup(self):
        if not IS_PYPY:
            for k in dir(self.__class__):
                if 'time' in k and 'numba' in k:
                    c = getattr(self, k)
                    c()

class TimeAtmosphereSuite(BaseTimeSuite):
    def setup(self):
        if not IS_PYPY:
            self.time_ATMOSPHERE_1976_numba()
        self.date_test_es = datetime(2020, 6, 6, 10, 0, 0, 0)
        self.tz_dt = pytz.timezone('Australia/Perth').localize(datetime(2020, 6, 6, 7, 10, 57))
        self.tz_dt2 = pytz.timezone('America/Edmonton').localize(datetime(2018, 4, 15, 13, 43, 5))



    def time_ATMOSPHERE_1976(self):
        ATMOSPHERE_1976(5000.0)

    def time_ATMOSPHERE_1976_numba(self):
        ATMOSPHERE_1976_numba(5000.0)
        
    def time_ATMOSPHERE_1976_pressure_integral(self):
        ATMOSPHERE_1976.pressure_integral(288.6, 84100.0, 147.0)
        
    def time_ATMOSPHERE_NRLMSISE00(self):
        ATMOSPHERE_NRLMSISE00(1E3, 45, 45, 150)
        
    def time_airmass(self):
        airmass(lambda Z : ATMOSPHERE_1976(Z).rho, 90.0)
        
    def time_airmass_numba(self):
        airmass_numba(numba_int_airmass, 90.0)
        
    def time_earthsun_distance(self):
        earthsun_distance(self.date_test_es)
    
    def time_solar_position(self):
        solar_position(self.tz_dt, -31.95265, 115.85742)
        
    def time_sunrise_sunset(self):
        sunrise_sunset(self.tz_dt, 51.0486, -114.07)
        
    def time_solar_irradiation(self):
        solar_irradiation(Z=1100.0, latitude=51.0486, longitude=-114.07, linke_turbidity=3, moment=self.tz_dt2, surface_tilt=41.0, surface_azimuth=180.0)


from fluids import isothermal_gas, isentropic_work_compression, isentropic_efficiency, P_isothermal_critical_flow
if not IS_PYPY:
    isentropic_work_compression_numba = fluids.numba.isentropic_work_compression
    isentropic_efficiency_numba = fluids.numba.isentropic_efficiency
    P_isothermal_critical_flow_numba = fluids.numba.P_isothermal_critical_flow
    isothermal_gas_numba = fluids.numba.isothermal_gas


class TimeCompressibleSuite(BaseTimeSuite):
    def setup(self):
        if not IS_PYPY:
            self.time_isentropic_work_compression_numba()
            self.time_isentropic_efficiency_numba()
            #self.time_P_isothermal_critical_flow_numba()
            self.time_compressible_D_numba()
            #self.time_compressible_P1_numba()
            #self.time_compressible_P2_numba()

    def time_compressible_D(self):
        isothermal_gas(rho=11.3, fd=0.00185, P1=1E6, P2=9E5, L=1000, m=145.48475726, D=None)

    def time_compressible_D_numba(self):
        isothermal_gas_numba(rho=11.3, fd=0.00185, P1=1E6, P2=9E5, L=1000, m=145.48475726, D=None)

    def time_compressible_P1(self):
        isothermal_gas(rho=11.3, fd=0.00185, P2=9E5, L=1000, m=145.48475726, D=0.5)

    #def time_compressible_P1_numba(self):
        #isothermal_gas_numba(rho=11.3, fd=0.00185, P2=9E5, L=1000, m=145.48475726, D=0.5)
        
    def time_compressible_P2(self):
        isothermal_gas(rho=11.3, fd=0.00185, P1=1E6, L=1000, m=145.48475726, D=0.5)

    #def time_compressible_P2_numba(self):
        #isothermal_gas_numba(rho=11.3, fd=0.00185, P1=1E6, L=1000, m=145.48475726, D=0.5)
        
    def time_isentropic_work_compression(self):
        isentropic_work_compression(P1=1E5, P2=1E6, T1=300.0, k=1.4, eta=0.78)
        
    def time_isentropic_work_compression_numba(self):
        isentropic_work_compression_numba(P1=1E5, P2=1E6, T1=300.0, k=1.4, eta=0.78)
        
    def time_isentropic_efficiency(self):
        isentropic_efficiency(1E5, 1E6, 1.4, eta_p=0.78)
        
    def time_isentropic_efficiency_numba(self):
        isentropic_efficiency_numba(1E5, 1E6, 1.4, eta_p=0.78)
        
    def time_P_isothermal_critical_flow(self):
        P_isothermal_critical_flow(P=1E6, fd=0.00185, L=1000., D=0.5)
        
    #def time_P_isothermal_critical_flow_numba(self):
        #P_isothermal_critical_flow_numba(P=1E6, fd=0.00185, L=1000., D=0.5)
        
        
from fluids import control_valve_noise_g_2011, control_valve_noise_l_2015, size_control_valve_l, size_control_valve_g

class TimeControlValveSuite(BaseTimeSuite):
    def setup(self):
        pass
    
    def time_size_control_valve_g(self):
        size_control_valve_g(T=433., MW=44.01, mu=1.4665E-4, gamma=1.30,  Z=0.988, P1=680E3, P2=310E3, Q=38/36., D1=0.08, D2=0.1, d=0.05, FL=0.85, Fd=0.42, xT=0.60)

    def time_size_control_valve_l(self):
        size_control_valve_l(rho=965.4, Psat=70.1E3, Pc=22120E3, mu=3.1472E-4, P1=680E3, P2=220E3, Q=0.1, D1=0.15, D2=0.15, d=0.15, FL=0.9, Fd=0.46)
        
    def time_control_valve_noise_l_2015(self):
        control_valve_noise_l_2015(m=40, P1=1E6, P2=6.5E5, Psat=2.32E3, rho=997, c=1400, Kv=77.848, d=0.1, Di=0.1071, FL=0.92, Fd=0.42, t_pipe=0.0036, rho_pipe=7800.0, c_pipe=5000.0,rho_air=1.293, c_air=343.0, An=-4.6)
        
    def time_control_valve_noise_g_2011(self):
        control_valve_noise_g_2011(m=2.22, P1=1E6, P2=7.2E5, T1=450, rho=5.3, gamma=1.22, MW=19.8, Kv=77.85,  d=0.1, Di=0.2031, FL=None, FLP=0.792, FP=0.98, Fd=0.296, t_pipe=0.008, rho_pipe=8000.0, c_pipe=5000.0, rho_air=1.293, c_air=343.0, An=-3.8, Stp=0.2)
        
        
from fluids import drag_sphere, v_terminal, integrate_drag_sphere

if not IS_PYPY:
    drag_sphere_numba = fluids.numba.drag_sphere
    v_terminal_numba = fluids.numba.v_terminal
#integrate_drag_sphere_numba = fluids.numba.integrate_drag_sphere


class TimeDragSuite(BaseTimeSuite):
    
    def time_drag_sphere(self):
        drag_sphere(20000.0, 'Barati_high')

    def time_drag_sphere_numba(self):
        drag_sphere_numba(20000.0, 'Barati_high')
        
    def time_v_terminal(self):
        v_terminal(D=70E-6, rhop=2600., rho=1000., mu=1E-3)

    def time_v_terminal_numba(self):
        v_terminal_numba(D=70E-6, rhop=2600., rho=1000., mu=1E-3)
        
    def time_integrate_drag_sphere(self):
        integrate_drag_sphere(D=0.001, rhop=2200., rho=1.2, mu=1.78E-5, t=0.5, V=30, distance=True)

from fluids import change_K_basis, entrance_distance, Darby3K, Hooper2K, K_angle_valve_Crane, v_lift_valve_Crane, K_branch_converging_Crane
if not IS_PYPY:

    change_K_basis_numba = fluids.numba.change_K_basis
    entrance_distance_numba = fluids.numba.entrance_distance
    Darby3K_numba = fluids.numba.Darby3K
    Hooper2K_numba = fluids.numba.Hooper2K
    K_angle_valve_Crane_numba = fluids.numba.K_angle_valve_Crane
    v_lift_valve_Crane_numba = fluids.numba.v_lift_valve_Crane
    K_branch_converging_Crane_numba = fluids.numba.K_branch_converging_Crane


class TimeFittingsSuite(BaseTimeSuite):
    #def setup(self):
        #pass
        #self.time_change_K_basis_numba()
        #self.time_entrance_distance_idelchik_numba()
        #self.time_entrance_distance_harris_numba()
        #self.time_Darby3K_numba()
        #self.time_Hooper2K_numba()

    def time_change_K_basis(self):
        change_K_basis(K1=32.68875692997804, D1=.01, D2=.02)

    def time_change_K_basis_numba(self):
        change_K_basis_numba(K1=32.68875692997804, D1=.01, D2=.02)
        
    def time_entrance_distance_idelchik(self):
        entrance_distance(Di=0.1, t=0.0005, l=.02, method='Idelchik')

    def time_entrance_distance_idelchik_numba(self):
        entrance_distance_numba(Di=0.1, t=0.0005, l=.02, method='Idelchik')

    def time_entrance_distance_harris(self):
        entrance_distance(Di=0.1, t=0.0005, l=.02, method='Harris')

    def time_entrance_distance_harris_numba(self):
        entrance_distance_numba(Di=0.1, t=0.0005, l=.02, method='Harris')
        
    def time_Darby3K(self):
        Darby3K(NPS=2., Re=10000., name='Valve, Angle valve, 45°, full line size, β = 1')

    def time_Darby3K_numba(self):
        Darby3K_numba(NPS=2., Re=10000., name='Valve, Angle valve, 45°, full line size, β = 1')
        
    def time_Hooper2K(self):
         Hooper2K(Di=2., Re=10000., name='Valve, Globe, Standard')

    def time_Hooper2K_numba(self):
         Hooper2K_numba(Di=2., Re=10000., name='Valve, Globe, Standard')
         
    def time_K_angle_valve_Crane(self):
         K_angle_valve_Crane(.01, .02)

    def time_K_angle_valve_Crane_numba(self):
         K_angle_valve_Crane_numba(.01, .02)
         
    def time_v_lift_valve_Crane(self):
        v_lift_valve_Crane(rho=998.2, D1=0.0627, D2=0.0779, style='lift check straight')

    def time_v_lift_valve_Crane_numba(self):
        v_lift_valve_Crane_numba(rho=998.2, D1=0.0627, D2=0.0779, style='lift check straight')

    def time_K_branch_converging_Crane(self):
        K_branch_converging_Crane(0.1023, 0.1023, 0.018917, 0.00633)

    def time_K_branch_converging_Crane_numba(self):
        K_branch_converging_Crane_numba(0.1023, 0.1023, 0.018917, 0.00633)


from fluids import C_Reader_Harris_Gallagher, differential_pressure_meter_solver, dP_venturi_tube
if not IS_PYPY:
    C_Reader_Harris_Gallagher_numba = fluids.numba.C_Reader_Harris_Gallagher
    differential_pressure_meter_solver_numba = fluids.numba.differential_pressure_meter_solver
    dP_venturi_tube_numba = fluids.numba.dP_venturi_tube

class TimeFlowMeterSuite(BaseTimeSuite):

    def time_C_Reader_Harris_Gallagher(self):
        C_Reader_Harris_Gallagher(D=0.07391, Do=0.0222, rho=1.165, mu=1.85E-5, m=0.12, taps='flange')
    
    def time_C_Reader_Harris_Gallagher_numba(self):
        C_Reader_Harris_Gallagher_numba(D=0.07391, Do=0.0222, rho=1.165, mu=1.85E-5, m=0.12, taps='flange')
        
    def time_dP_venturi_tube(self):
        dP_venturi_tube(D=0.07366, Do=0.05, P1=200000.0, P2=183000.0)
        
    def time_dP_venturi_tube_numba(self):
        dP_venturi_tube_numba(D=0.07366, Do=0.05, P1=200000.0, P2=183000.0)

    def time_differential_pressure_meter_solver_m(self):
        differential_pressure_meter_solver(D=0.07366, D2=0.05, P1=200000.0, P2=183000.0, rho=999.1, mu=0.0011, k=1.33, meter_type='ISO 5167 orifice', taps='D')

    def time_differential_pressure_meter_solver_numba_m(self):
        differential_pressure_meter_solver_numba(D=0.07366, D2=0.05, P1=200000.0, P2=183000.0, rho=999.1, mu=0.0011, k=1.33, meter_type='ISO 5167 orifice', taps='D')
        
    def time_differential_pressure_meter_solver_P2(self):
        differential_pressure_meter_solver(D=0.07366, D2=0.05, P1=200000.0, m=7.702338035732167, rho=999.1, mu=0.0011, k=1.33, meter_type='ISO 5167 orifice', taps='D')

    def time_differential_pressure_meter_solver_numba_P2(self):
        differential_pressure_meter_solver_numba(D=0.07366, D2=0.05, P1=200000.0, m=7.702338035732167, rho=999.1, mu=0.0011, k=1.33, meter_type='ISO 5167 orifice', taps='D')
        
    def time_differential_pressure_meter_solver_P1(self):
        differential_pressure_meter_solver(D=0.07366, D2=0.05, P2=183000.0, m=7.702338035732167, rho=999.1, mu=0.0011, k=1.33, meter_type='ISO 5167 orifice', taps='D')

    def time_differential_pressure_meter_solver_numba_P1(self):
        differential_pressure_meter_solver_numba(D=0.07366, D2=0.05, P2=183000.0, m=7.702338035732167, rho=999.1, mu=0.0011, k=1.33, meter_type='ISO 5167 orifice', taps='D')

    def time_differential_pressure_meter_solver_D2(self):
        differential_pressure_meter_solver(D=0.07366, P1=200000.0, P2=183000.0, m=7.702338035732167, rho=999.1, mu=0.0011, k=1.33, meter_type='ISO 5167 orifice', taps='D')

    def time_differential_pressure_meter_solver_numba_D2(self):
        differential_pressure_meter_solver_numba(D=0.07366, P1=200000.0, P2=183000.0, m=7.702338035732167, rho=999.1, mu=0.0011, k=1.33, meter_type='ISO 5167 orifice', taps='D')
        
        
        
    def time_differential_pressure_meter_solver_m_Hollingshead(self):
        differential_pressure_meter_solver(D=0.07366, D2=0.05, P1=200000.0, P2=183000.0, rho=999.1, mu=0.0011, k=1.33, meter_type='Hollingshead orifice', taps='D')

    def time_differential_pressure_meter_solver_numba_m_Hollingshead(self):
        differential_pressure_meter_solver_numba(D=0.07366, D2=0.05, P1=200000.0, P2=183000.0, rho=999.1, mu=0.0011, k=1.33, meter_type='Hollingshead orifice', taps='D')
        
    def time_differential_pressure_meter_solver_P2_Hollingshead(self):
        differential_pressure_meter_solver(D=0.07366, D2=0.05, P1=200000.0, m=7.702338035732167, rho=999.1, mu=0.0011, k=1.33, meter_type='Hollingshead orifice', taps='D')

    def time_differential_pressure_meter_solver_numba_P2_Hollingshead(self):
        differential_pressure_meter_solver_numba(D=0.07366, D2=0.05, P1=200000.0, m=7.702338035732167, rho=999.1, mu=0.0011, k=1.33, meter_type='Hollingshead orifice', taps='D')
        
    def time_differential_pressure_meter_solver_P1_Hollingshead(self):
        differential_pressure_meter_solver(D=0.07366, D2=0.05, P2=183000.0, m=7.702338035732167, rho=999.1, mu=0.0011, k=1.33, meter_type='Hollingshead orifice', taps='D')

    def time_differential_pressure_meter_solver_numba_P1_Hollingshead(self):
        differential_pressure_meter_solver_numba(D=0.07366, D2=0.05, P2=183000.0, m=7.702338035732167, rho=999.1, mu=0.0011, k=1.33, meter_type='Hollingshead orifice', taps='D')

    def time_differential_pressure_meter_solver_D2_Hollingshead(self):
        differential_pressure_meter_solver(D=0.07366, P1=200000.0, P2=183000.0, m=7.702338035732167, rho=999.1, mu=0.0011, k=1.33, meter_type='Hollingshead orifice', taps='D')

    def time_differential_pressure_meter_solver_numba_D2_Hollingshead(self):
        differential_pressure_meter_solver_numba(D=0.07366, P1=200000.0, P2=183000.0, m=7.702338035732167, rho=999.1, mu=0.0011, k=1.33, meter_type='Hollingshead orifice', taps='D')



        
    def time_differential_pressure_meter_solver_m_Miller_orifice(self):
        differential_pressure_meter_solver(D=0.07366, D2=0.05, P1=200000.0, P2=183000.0, rho=999.1, mu=0.0011, k=1.33, meter_type='Miller orifice', taps='corner')

    def time_differential_pressure_meter_solver_numba_m_Miller_orifice(self):
        differential_pressure_meter_solver_numba(D=0.07366, D2=0.05, P1=200000.0, P2=183000.0, rho=999.1, mu=0.0011, k=1.33, meter_type='Miller orifice', taps='corner')
        
    def time_differential_pressure_meter_solver_P2_Miller_orifice(self):
        differential_pressure_meter_solver(D=0.07366, D2=0.05, P1=200000.0, m=7.702338035732167, rho=999.1, mu=0.0011, k=1.33, meter_type='Miller orifice', taps='corner')

    def time_differential_pressure_meter_solver_numba_P2_Miller_orifice(self):
        differential_pressure_meter_solver_numba(D=0.07366, D2=0.05, P1=200000.0, m=7.702338035732167, rho=999.1, mu=0.0011, k=1.33, meter_type='Miller orifice', taps='corner')
        
    def time_differential_pressure_meter_solver_P1_Miller_orifice(self):
        differential_pressure_meter_solver(D=0.07366, D2=0.05, P2=183000.0, m=7.702338035732167, rho=999.1, mu=0.0011, k=1.33, meter_type='Miller orifice', taps='corner')

    def time_differential_pressure_meter_solver_numba_P1_Miller_orifice(self):
        differential_pressure_meter_solver_numba(D=0.07366, D2=0.05, P2=183000.0, m=7.702338035732167, rho=999.1, mu=0.0011, k=1.33, meter_type='Miller orifice', taps='corner')

    def time_differential_pressure_meter_solver_D2_Miller_orifice(self):
        differential_pressure_meter_solver(D=0.07366, P1=200000.0, P2=183000.0, m=7.702338035732167, rho=999.1, mu=0.0011, k=1.33, meter_type='Miller orifice', taps='corner')

    def time_differential_pressure_meter_solver_numba_D2_Miller_orifice(self):
        differential_pressure_meter_solver_numba(D=0.07366, P1=200000.0, P2=183000.0, m=7.702338035732167, rho=999.1, mu=0.0011, k=1.33, meter_type='Miller orifice', taps='corner')

    

    

suites = [TimeAtmosphereSuite, TimeCompressibleSuite, TimeControlValveSuite, TimeDragSuite, TimeFittingsSuite, TimeFlowMeterSuite]
                
for suite in suites:
    continue
    # asv requires inspect to work :(
    # Do I want to write a file that writes this benchmark file?
    glbs, lcls = {}, {}
    for k in dir(suite):
        if 'time' in k:
            f = getattr(suite, k)
            if hasattr(f, 'duplicate_with_numba'):
                source = inspect.getsource(f)
                source = '\n'.join([s[4:] for s in source.split('\n')[1:]])
                orig_function = k.replace('time_', '')
                numba_function = orig_function + '_numba'
                new_function_name = k + '_numba'
                new_source = source.replace(orig_function, numba_function)
                exec(new_source, glbs, lcls)
                setattr(suite, new_function_name, lcls[new_function_name])

if IS_PYPY:
    for s in suites:
        for k in dir(s):
            if 'time' in k and 'numba' in k:
                delattr(s, k)
                
