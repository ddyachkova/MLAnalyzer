import numpy as np
import ROOT
from root_numpy import root2array, tree2array
#from root_pandas.readwrite import convert_to_dataframe
from dask.delayed import delayed
import dask.array as da
import dask.dataframe as df
import h5py

#eosDir='/eos/cms/store/user/mandrews/ML/IMGs'
eosDir='/eos/cms/store/user/mandrews/ML/IMGs_RAW'
decays = [
    "SinglePhotonPt50",
    "SingleElectronPt50"
    ]
s = 32
crop_size = int(s*s)
chunk_size = 9960
n_channels = 14
ver = 1

chunk_shape = (chunk_size,n_channels,crop_size)

@delayed
def process_chunk(x):

    E_scale = 50.
    t_scale = 50.

    # Energy
    Efull = x[:,0,:]
    Efull /= E_scale
    # Time
    tfull = x[:,1,:]
    tfull /= t_scale

    # Energy
    E = x[:,2,:]
    E /= E_scale
    # Time
    t = x[:,3,:]
    t /= t_scale

    rh = np.stack([Efull, tfull, E, t], axis=1)

    adc_off = 2.3

    # Noise
    noise = np.mean(x[:,4:7,:], axis=1)
    noise = np.expand_dims(noise, axis=1)

    # Digi
    digi = x[:,4:,:]
    pos = (digi > 0.)
    digi[pos] = np.log10(digi[pos]) - adc_off

    X = np.concatenate([rh, digi], axis=1)
    X = X.reshape((-1,X.shape[1],s,s))
    X = np.transpose(X, [0,2,3,1])

    return X

for j,decay in enumerate(decays):

    file_in_str = "%s/%s_IMGCROPS_n249k.hdf5"%(eosDir,decay)
    dset = h5py.File(file_in_str)
    X_in = da.from_array(dset['/X'], chunks=chunk_shape)
    y_in = da.from_array(dset['/y'], chunks=(chunk_size,))
    assert X_in.shape[0] == y_in.shape[0]
    events = X_in.shape[0]
    #events = 10000
    assert events % chunk_size == 0
    print " >> Doing decay:", decay
    print " >> Input file:", file_in_str
    print " >> Total events:", events

    print " >> Processing..."
    X = da.concatenate([da.from_delayed(\
                        process_chunk(X_in[i:i+chunk_size]),\
                        shape=(chunk_size,s,s,14),\
                        dtype=np.float32)\
                        for i in range(0,events,chunk_size)])

    file_out_str = "%s/%s_IMGCROPS_n249k_RHv1+DIGIv5.hdf5"%(eosDir,decay)
    print " >> Writing to:", file_out_str
    da.to_hdf5(file_out_str, {'/X': X, '/y': y_in}, compression='lzf')

    print " >> Done.\n"
