def Enable_throttle_AGG():
cdie.soc_cr_wrapper.pd_infra_pdn.dfvfcr_pd_infra_fuse.dfvfcr_pd_infra_fuse.dfvfreg5.ipu_throttleip_disable =   0x0
cdie.soc_cr_wrapper.pd_infra_pdn.dfvfcr_pd_infra_fuse.dfvfcr_pd_infra_fuse.dfvfreg5.vpu_throttleip_disable =   0x0
cdie.soc_cr_wrapper.pd_infra_pdn.dfvfcr_pd_infra_fuse.dfvfcr_pd_infra_fuse.dfvfreg5.iax_throttleip_disable =   0x0
cdie.soc_cr_wrapper.pd_infra_pdn.dfvfcr_pd_infra_fuse.dfvfcr_pd_infra_fuse.dfvfreg5.media_throttleip_disable = 0x0
cdie.soc_cr_wrapper.pd_infra_pdn.dfvfcr_pd_infra_fuse.dfvfcr_pd_infra_fuse.dfvfreg5.gt_throttleip_disable =    0x0
cdie.soc_cr_wrapper.pd_infra_pdn.dfvfcr_pd_infra_fuse.dfvfcr_pd_infra_fuse.dfvfreg5.atom_throttleip_disable =  0x0
cdie.soc_cr_wrapper.pd_infra_pdn.dfvfcr_pd_infra_fuse.dfvfcr_pd_infra_fuse.dfvfreg5.core0_throttleip_disable = 0x0
cdie.soc_cr_wrapper.pd_infra_pdn.dfvfcr_pd_infra_fuse.dfvfcr_pd_infra_fuse.dfvfreg5.core1_throttleip_disable = 0x0
cdie.soc_cr_wrapper.pd_infra_pdn.dfvfcr_pd_infra_fuse.dfvfcr_pd_infra_fuse.dfvfreg5.core2_throttleip_disable = 0x0
cdie.soc_cr_wrapper.pd_infra_pdn.dfvfcr_pd_infra_fuse.dfvfcr_pd_infra_fuse.dfvfreg5.core3_throttleip_disable = 0x0

def Disable_throttle_By_Domain(Domain):
cdie.soc_cr_wrapper.pd_infra_pdn.dfvfcr_pd_infra_fuse.dfvfcr_pd_infra_fuse.dfvfreg5.ipu_throttleip_disable


finish = ['ipu_throttleip_disable', 'vpu_throttleip_disable','iax_throttleip_disable','media_throttleip_disable',
          'gt_throttleip_disable', 'atom_throttleip_disable','core0_throttleip_disable', 'core1_throttleip_disable',
          'core2_throttleip_disable', 'core3_throttleip_disable']

for i in range(5):
    command = 'cdie.soc_cr_wrapper.pd_infra_pdn.dfvfcr_pd_infra_fuse.dfvfcr_pd_infra_fuse.dfvfreg5.' + finish[i]
    exec(command)

