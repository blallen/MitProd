#include "MitProd/TreeFiller/interface/FillerVertexes.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "MitAna/DataTree/interface/Names.h"
#include "MitAna/DataTree/interface/VertexCol.h"
#include "MitProd/ObjectService/interface/ObjectService.h"
#include "MitEdm/DataFormats/interface/RefToBaseToPtr.h"

using namespace std;
using namespace edm;
using namespace mithep;

//--------------------------------------------------------------------------------------------------
FillerVertexes::FillerVertexes(const ParameterSet &cfg, edm::ConsumesCollector& collector, ObjectService* os, const char *name, bool active) : 
  BaseFiller(cfg,os,name,active),
  edmToken_(GetToken<reco::VertexCollection>(collector, "edmName","offlinePrimaryVertices")),
  mitName_(Conf().getUntrackedParameter<string>("mitName","PrimaryVertexes")),
  trackMapName_(Conf().getUntrackedParameter<string>("trackMapName","")),
  vertexMapName_(Conf().getUntrackedParameter<string>("vertexMapName","VertexMap")),
  vertexes_(new mithep::VertexArr(100)),
  vertexMap_(new mithep::VertexMap),
  trackMap_(0)
{
  // Constructor.
}

//--------------------------------------------------------------------------------------------------
FillerVertexes::~FillerVertexes()
{
  // Destructor.

  delete vertexes_;
  delete vertexMap_;
}

//--------------------------------------------------------------------------------------------------
void FillerVertexes::BookDataBlock(TreeWriter &tws)
{
  // Add Vertex branch and the VertexMap to tree.

  tws.AddBranch(mitName_,&vertexes_);
  OS()->add<VertexArr>(vertexes_,mitName_);

  if (!vertexMapName_.empty()) {
    vertexMap_->SetBrName(mitName_);
    OS()->add<VertexMap>(vertexMap_,vertexMapName_);
  }
  if (!trackMapName_.empty()) {
    trackMap_ = OS()->get<TrackMap>(trackMapName_);
    if (trackMap_)
      AddBranchDep(mitName_,trackMap_->GetBrName());
  }
}

//--------------------------------------------------------------------------------------------------
void FillerVertexes::FillDataBlock(const edm::Event      &event, 
                                   const edm::EventSetup &setup)
{
  // Fill the Vertex branch.

  vertexes_->Delete();
  vertexMap_->Reset();

  Handle<reco::VertexCollection> hVertexProduct;
  GetProduct(edmToken_, hVertexProduct, event);
  vertexMap_->SetEdmProductId(hVertexProduct.id().id());
  reco::VertexCollection const& inVertexes = *hVertexProduct;

  // loop through all vertexes
  for (reco::VertexCollection::const_iterator inV = inVertexes.begin(); 
       inV != inVertexes.end(); ++inV) {

    mithep::Vertex *outVertex = vertexes_->Allocate();
    new (outVertex) mithep::Vertex(inV->x(), inV->y(), inV->z(),
                                   inV->xError(), inV->yError(), inV->zError());
    outVertex->SetChi2(inV->chi2());
    outVertex->SetIsValid(inV->isValid());
    outVertex->SetNdof(inV->ndof());
    outVertex->SetNTracksFit(inV->tracksSize());

    //fill tracks associated to the vertex
    if (trackMap_) {
      for (reco::Vertex::trackRef_iterator iTrack = inV->tracks_begin(); iTrack!=inV->tracks_end(); ++iTrack) {
        outVertex->AddTrack(trackMap_->GetMit(mitedm::refToBaseToPtr(*iTrack)), inV->trackWeight(*iTrack));
      }
    }

    //add vertex to the map
    mitedm::VertexPtr thePtr(hVertexProduct, inV-inVertexes.begin());
    vertexMap_->Add(thePtr, outVertex);
         
  }
  vertexes_->Trim();
}

DEFINE_MITHEP_TREEFILLER(FillerVertexes);
