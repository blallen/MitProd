// $Id: FillerMCVertexes.cc,v 1.17 2009/07/20 03:19:24 loizides Exp $

#include "MitProd/TreeFiller/interface/FillerMCVertexes.h"
#include "MitAna/DataTree/interface/Names.h"
#include "MitAna/DataTree/interface/VertexCol.h"
#include "MitProd/ObjectService/interface/ObjectService.h"

using namespace std;
using namespace edm;
using namespace mithep;

//--------------------------------------------------------------------------------------------------
FillerMCVertexes::FillerMCVertexes(const ParameterSet &cfg, const char *name, bool active) : 
  BaseFiller(cfg, name, active),
  useAodGen_(Conf().getUntrackedParameter<bool>("useAodGen",true)),
  edmName_(Conf().getUntrackedParameter<string>("edmName","genParticles")),
  mitName_(Conf().getUntrackedParameter<string>("mitName","MCVertexes")),
  vertexes_(new mithep::VertexArr(1))
{
  // Constructor.
}

//--------------------------------------------------------------------------------------------------
FillerMCVertexes::~FillerMCVertexes()
{
  // Destructor.

  delete vertexes_;
}

//--------------------------------------------------------------------------------------------------
void FillerMCVertexes::BookDataBlock(TreeWriter &tws, const edm::EventSetup &es)
{
  // Add branch to tree.

  tws.AddBranch(mitName_,&vertexes_);
  OS()->add<VertexArr>(vertexes_,mitName_);
}

//--------------------------------------------------------------------------------------------------
void FillerMCVertexes::FillDataBlock(const edm::Event      &event, 
                                     const edm::EventSetup &setup)
{
  // Loop over generated or simulated particles and fill their information.

  vertexes_->Delete();

  Double_t vtx=0, vty=0, vtz=0;

  if (!useAodGen_) {
    Handle<edm::HepMCProduct> hHepMCProduct;
    GetProduct(edmName_, hHepMCProduct, event);
    const HepMC::GenEvent &GenEvent = hHepMCProduct->getHepMCData();  

    for (HepMC::GenEvent::particle_const_iterator pgen = GenEvent.particles_begin();
        pgen != GenEvent.particles_end(); ++pgen) {
      HepMC::GenParticle *mcPart = (*pgen);
      if(!mcPart) 
        continue;
      HepMC::GenVertex *dvtx = mcPart->end_vertex();
      if (dvtx) {
        vtx = dvtx->point3d().x()/10.0;
        vty = dvtx->point3d().y()/10.0;
        vtz = dvtx->point3d().z()/10.0;
        break;
      }
    }  
  } else { /*useAodGen_*/
    Handle<reco::GenParticleCollection> hGenPProduct;
    GetProduct(edmName_, hGenPProduct, event);  
    const reco::GenParticleCollection genParticles = *(hGenPProduct.product());  
    for (reco::GenParticleCollection::const_iterator pgen = genParticles.begin();
        pgen != genParticles.end(); ++pgen) {

      int found = 0;
      for (unsigned int i=0; i<pgen->numberOfDaughters(); ++i) {
        const reco::Candidate *dau = pgen->daughter(i);
        if (dau) {
          vtx = dau->vx();
          vty = dau->vy();
          vtz = dau->vz();
          found = 1;
          break;
        }
      }
      if (found)
        break;
    }
  }

  mithep::Vertex *newvtx = vertexes_->Allocate();
  new (newvtx) mithep::Vertex(vtx, vty, vtz);
  vertexes_->Trim();
}